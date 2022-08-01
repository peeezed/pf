# use regex to find timer

import pytesseract as tess
from PIL import Image
import pyscreenshot as ImageGrab
import re

def get_remaining_time(aspect_ratio = ()):
    x2 = int(aspect_ratio[0]/2)
    y2 = aspect_ratio[1]
    im=ImageGrab.grab(bbox=(0,0,x2,y2))
    #im.show()
    new_img = im.resize(((x2)*3,(y2)*3))
    text = tess.image_to_string(new_img)
    #print(text)
    #new_img.show()
    time_regex  = re.compile(
        r"(TIME\sREMAINING)(\s)?(\d)*(\s)?(hours)*(\s)?(\d)*(\s)?(minutes)*(\s)?(\d)*(\s)?(seconds)*"
        )
    match_object = time_regex.search(text)
    if match_object:
        matched_timer = match_object.group()
        #print(match_object.group())
        timer = matched_timer.split("TIME REMAINING")[1]
        #print(timer)
        return timer
