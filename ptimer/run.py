import eel
import time
import datetime
import os
import timeit

from backend import Database
from tkinter import *
from tkinter import filedialog
from shutil import copy2

eel.init("web")

"""
@eel.expose
def hello(place):
    print("called from: " + place)

@eel.expose
def sort(text):
    answer = sorted([float(num) for num in text.split(",")])
    eel.showAnswers(answer)"""

@eel.expose
def countdown(t, now=datetime.datetime.now):
    target = now()
    one_second_later = datetime.timedelta(seconds = 1)
    mins,secs = divmod(t,60)
    eel.showCountdown(mins, secs, t)
    
    for remaining in range(t, -1, -1):
        target += one_second_later
        if eel.isPaused()():
            break
        mins,secs = divmod(t,60)
        eel.showCountdown(mins, secs, t)
        print("target: ",target)
        print("now: ",now())
        print("target - now: ",(target-now()).total_seconds())
        time.sleep((target - now()).total_seconds())
        t -= 1

db = Database("data/exercises.db")

@eel.expose
def save_exercises(exerciseName, bpm):
    root = Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    file_path = filedialog.askopenfile(initialdir=os.path.expanduser("~/Desktop"),
    title="Select Exercise",
    filetypes= (("jpeg files","*.jpg"), ("png files","*.png"), ("svg files", "*.svg"))
    )
    try:
        file_to_save = file_path.name
        name_to_url = "exercises/" + file_to_save.split("/")[-1]
        save_directory = "web/exercises"
        copy2(file_to_save, save_directory)
        db.add_exercise(exerciseName, bpm, name_to_url)
    except AttributeError:
        pass

@eel.expose
def delete_exercise(_id):
    try:
        db.delete_exercise(_id)
        print("Entry Deleted")
    except:
        print("An error ocurred")

@eel.expose
def update_exercise(_id, name, bpm):
    try:
        db.update_exercise(_id,name,bpm)
        print("Entry Updated")
    except:
        print("An error occured.")

# save_exercises("ben keno",130)

@eel.expose
def relay_exercises(add_dropdown=False):
    exercises = []
    for _id, name, bpm, url in db.get_exercises():
        exercises.append([name,bpm,url,_id])
    # print(exercises)
    eel.addExercises(exercises)
    if add_dropdown:
        eel.addDropdown()


eel.start("main.html")
"""
while True:
    timestamp = dt.now()
    eel.addText(f"the time is {timestamp.strftime('%I:%M:%S %p')}")

    eel.sleep(1.0)
"""
