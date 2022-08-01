# specify the timer =>
# shut down the pc after timer reaches to 0 =>
# use image recognition, and-or image to text to automate the timer proccess first from steam =>
# after we understand how it works we can do it to gog, origin and uplay aswell
# potentially use a gui

import datetime
import time
import os
import re
from screen_reader import get_remaining_time
from settings import Settings

settings = Settings()

def time_to_seconds(time): # 1h 1h20m 20m 1hour 1hours 20minutes 20 mins 20 min
    time = time.lower()
    time = time.replace(" ","")
    hour_handles = ["hours","hour"]
    minute_handles = ["minutes", "minute", "mins", "min"]
    for word in hour_handles:
        if word in time:
            time = time.replace(f"{word}","h")
    for word in minute_handles:
        if word in time:
            time = time.replace(f"{word}","m")
    if "h" in time and "m" not in time:
        hour = time.split("h")[0]
        timer = int(hour)*3600
    if "h" in time and "m" in time:
        hour = time.split("h")[0]
        minute = time.split("h")[1].split("m")[0]
        timer = int(hour)*3600 + int(minute)*60
    if "m" in time and "h" not in time:
        minute = time.split("m")[0]
        timer = int(minute)*60
    return timer

def shutdown_computer(timer): # in seconds
    #print("shutting down in "+ str(timer)) # to test without shutting down the computer
    shutdown_time = timer + settings.extra_time
    print("Shutdown in: " + str(shutdown_time/60) + " minutes, press 'CTRL + C' to disable.")
    time.sleep(shutdown_time)
    os.system("shutdown /s /t 1")

def run():
    choice = input("Please set shutdown timer, or write 'Steam', to exit write 'exit': ")
    if choice.lower() == "exit":
        exit()
    if choice.lower() == "steam": 
        input("Make Steam full screen and make sure remaining time is visible, and press enter to continue")
        shutdown_computer(time_to_seconds(get_remaining_time(aspect_ratio=(settings.aspect_ratio_x,settings.aspect_ratio_y))))
    else:
        try:
            shutdown_computer(time_to_seconds(choice))
        except:
            run()

if __name__ == "__main__":
    run()
