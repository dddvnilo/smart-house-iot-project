import random
import time

class Infrared_receiver_simulator(object):
    def __init__(self,settings,callback, publish_event):
        self.pin = settings["pin"]
        self.scan_delay = settings["scan_delay"]
        self.callback = callback

        self.settings = settings
        self.publish_event = publish_event

        self.Buttons = [0x300ff22dd, 0x300ffc23d, 0x300ff629d, 0x300ffa857, 0x300ff9867, 0x300ffb04f, 0x300ff6897, 0x300ff02fd, 0x300ff30cf, 0x300ff18e7, 0x300ff7a85, 0x300ff10ef, 0x300ff38c7, 0x300ff5aa5, 0x300ff42bd, 0x300ff4ab5, 0x300ff52ad]  # HEX code list
        self.ButtonsNames = ["LEFT",   "RIGHT",      "UP",       "DOWN",       "2",          "3",          "1",        "OK",        "4",         "5",         "6",         "7",         "8",          "9",        "*",         "0",        "#"]  # String list in same order as HEX list

    def pressed(self, button):
        self.callback(button, self.settings, self.publish_event)


def run_infrared_receiver_simulator(ir, stop_event):
    buttons = ["LEFT",   "RIGHT",      "UP",       "DOWN",       "2",          "3",       
            "1",        "OK",        "4",         "5",         "6",         "7", 
            "8",          "9",        "*",         "0",        "#"]

    while not stop_event.is_set():
        if random.random() < 0.2: # 20% sansa da se aktivira
            button = random.choice(buttons)
            ir.pressed(button)
        time.sleep(0.5)