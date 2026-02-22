import random
import time

class Membrane_keypad_simulator(object):
    def __init__(self,settings,callback, publish_event):
        self.pin_rows = settings["pin_rows"]
        self.pin_cols = settings["pin_cols"]
        self.scan_delay = settings["scan_delay"]
        self.callback = callback

        self.settings = settings
        self.publish_event = publish_event
        
    def keypad_pressed(self, keypad):
        self.callback(keypad, self.settings, self.publish_event)


def run_membrane_keypad_simulator(mk, stop_event):
    keys = ['1','2','3','A',
            '4','5','6','B',
            '7','8','9','C',
            '*','0','#','D']

    while not stop_event.is_set():
        if random.random() < 0.2: # 20% sansa da se aktivira
            key = random.choice(keys)
            mk.keypad_pressed(key)
        time.sleep(0.5)