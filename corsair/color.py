# import queue
import time
# import threading

from cuesdk import *

sdk = CueSdk()
sdk.connect()

def read_keys(input_queue):
    while True:
        input_str = input()
        input_queue.put(input_str)


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
    

colors = {
    "green" : (0,120,0),
    "yellow" : (120,120,0),
    "blue" : (0,0,120),
    "white" : (200,200,200),
    "meatball" : (200,0,0)
}

leds = get_available_leds()
print(sdk.protocol_details)
flag = True
duration = 5
while flag:
    for sec in range(0,duration):
        change_color(leds,colors["meatball"])
        time.sleep(1)
        print(sec)
        if sec == duration - 1:
            flag = False

# def main():
#     global sdk

#     input_queue = queue.Queue()
#     input_thread = threading.Thread(target=read_keys,
#                                     args=(input_queue, ),
#                                     daemon=True)
#     input_thread.start()
#     sdk = CueSdk()

#     connected = sdk.connect()
#     if not connected:
#         err = sdk.get_last_error()
#         print("Handshake failed: %s" % err)
#         return

#     leds = get_available_leds()

#     while True:
#         if input_queue.qsize() > 0:
#             input_str = input_queue.get()

#             if input_str.lower() == "q":
#                 print("Exiting.")
#                 break
#             elif input_str == "+":
#                 if wave_duration > 100:
#                     wave_duration -= 100
#             elif input_str == "-":
#                 if wave_duration < 2000:
#                     wave_duration += 100

#         change_color(leds)

#         time.sleep(0.01)

# if __name__ == "__main__":
#     main()