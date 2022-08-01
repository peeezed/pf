import irsdk
import time
import itertools
import sys
import socket
import configparser
import math
import threading
import urllib
import logging


class IracingClient(object):
    def __init__(self):
        self.checkered        = 0x0001
        self.white            = 0x0002
        self.green            = 0x0004
        self.yellow           = 0x0008
        self.red              = 0x0010
        self.blue             = 0x0020
        self.debris           = 0x0040
        self.crossed          = 0x0080
        self.yellow_waving    = 0x0100
        self.one_lap_to_green = 0x0200
        self.green_held       = 0x0400
        self.ten_to_go        = 0x0800
        self.five_to_go       = 0x1000
        self.random_waving    = 0x2000
        self.caution          = 0x4000
        self.caution_waving   = 0x8000
        self.black      = 0x010000
        self.disqualify = 0x020000
        self.servicible = 0x040000 # car is allowed service (not a flag)
        self.furled     = 0x080000
        self.repair     = 0x100000

        self.ir = irsdk.IRSDK()
        self.ir.startup()

    def get_flag(self):
        flag = self.ir["SessionFlags"]
        flag_name = "no flag"

        if flag & self.checkered:
            print("checkered")
            flag_name = "checkered"

        elif flag & self.yellow:
            print("yellow")
            flag_name = "yellow"

        elif flag & self.yellow_waving:
            print("yellow waving")
            flag_name = "yellow_waving"
            #make it flash

        elif flag & self.repair:
            print("repair")
            flag_name = "repair"

        elif flag & self.blue:
            print("blue flag")
            flag_name = "blue"

        elif flag & self.green:
            print("green flag")
            flag_name = "green"

        elif flag & self.white:
            print("white flag")
            flag_name = "white"
        
        elif flag & self.green_held:
            print("green held")
            flag_name = "green_held"
        
        elif flag & self.caution:
            print("caution")
            flag_name = "caution"
        
        elif flag & self.caution_waving:
            print("caution waving")
            flag_name = "caution_waving"

        elif flag & self.furled:
            flag_name = "furled"

        elif flag & self.black:
            flag_name = "black"

        print(flag_name)
        return flag_name

# client = IracingClient()
# client.get_flag()