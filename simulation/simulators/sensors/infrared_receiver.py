import random
import time

def run_infrared_receiver_simulator(callback, stop_event, publish_event, settings):
    buttons = ["LEFT",   "RIGHT",      "UP",       "DOWN",       "2",          "3",       
            "1",        "OK",        "4",         "5",         "6",         "7", 
            "8",          "9",        "*",         "0",        "#"]

    while not stop_event.is_set():
        if random.random() < 0.2: # 20% sansa da se aktivira
            button = random.choice(buttons)
            callback(button, settings, publish_event)
        time.sleep(0.25)