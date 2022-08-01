from ir_client import IracingClient
import time
from cuesdk import *

client = IracingClient()
sdk = CueSdk()
sdk.connect()

def get_available_leds():
    leds = list()
    device_count = sdk.get_device_count()

    for device_index in range(device_count):
        led_positions = sdk.get_led_positions_by_device_index(device_index)
        leds.append(led_positions)
    print(leds)
    return leds

def change_color(all_leds, color = (0,255,0)):
    cnt = len(all_leds)
    for di in range(cnt):
        device_leds = all_leds[di]
        for led in device_leds:
            device_leds[led] = color # Green.
        sdk.set_led_colors_buffer_by_device_index(di, device_leds)
    sdk.set_led_colors_flush_buffer()

def perform_pulse_effect(wave_duration, all_leds):
    time_per_frame = 25
    x = 0
    cnt = len(all_leds)
    dx = time_per_frame / wave_duration

    while x < 2:
        val = int((1 - (x - 1)**2) * 200)
        for di in range(cnt):
            device_leds = all_leds[di]
            for led in device_leds:
                device_leds[led] = (val ,val, val)  # Green.

            sdk.set_led_colors_buffer_by_device_index(di, device_leds)

        sdk.set_led_colors_flush_buffer()
        time.sleep(time_per_frame / 1000)
        print("poggers")
        x += dx


def perform_flash_effect(flash_frequency, all_leds, color = (0, 200, 0)):
    cnt = len(all_leds)
    freq = flash_frequency
    dark = (0,0,0)
    x = 0


    while x < 1:
        for di in range(cnt):
            device_leds = all_leds[di]
            for led in device_leds:
                device_leds[led] = color
            sdk.set_led_colors_buffer_by_device_index(di, device_leds)

        sdk.set_led_colors_flush_buffer()
        time.sleep(freq)
        for di in range(cnt):
            device_leds = all_leds[di]
            for led in device_leds:
                device_leds[led] = dark
            sdk.set_led_colors_buffer_by_device_index(di, device_leds)
        sdk.set_led_colors_flush_buffer()
        time.sleep(freq)
        x += 1
        print(x)

colors = {
    "green" : (0,120,5),
    # "green_held" : (0,255,0),
    "yellow" : (120,120,0),
    "yellow_waving" : (120,120,0),
    "blue" : (0,0,120),
    "white" : (200,200,200),
    "repair" : (255,69,0),
    "dark" : (0,0,0),
    "black" : (250,0,0),
    "furled" : (250,0,0),
    "checkered" : (200,200,200),
    "flash" : (100,100,100)
}

leds = get_available_leds()
# print(sdk.protocol_details)
# flag = True
# duration = 5
# while flag:
#     for sec in range(0,duration):
#         change_color(leds,colors["yellow"])
#         time.sleep(1)
#         print(sec)
#         if sec == duration - 1:
#             flag = False

if __name__ == "__main__":
    flashies = ["furled", "checkered", "yellow_waving","flash","repair"]
    try:
        while True:
            flag = client.get_flag()
            # print(flag)
            if flag == "no flag":
                # print("True")
                change_color(leds,colors["dark"])
            elif flag in flashies:
                # perform_pulse_effect(300, leds)
                # perform_flash_effect(.4, leds, colors[flag])
                change_color(leds,colors[flag])
                time.sleep(.3)
                change_color(leds,colors["dark"])
            else:
                try:
                    change_color(leds,colors[flag])
                except:
                    pass
            time.sleep(.3)
    except KeyboardInterrupt:
        pass