import random
import time

class Button_simulator(object):
    def __init__(self,settings,callback, publish_event):
        self.pin = settings["pin"]
        self.callback = callback
        self.settings = settings
        self.publish_event = publish_event
        
    def button_pressed_callback(self):
        self.callback(False, self.settings, self.publish_event)

    def button_released_callback(self):
        self.callback(True, self.settings, self.publish_event)


def run_button_simulator(button, stop_event):
    while not stop_event.is_set():
        if random.random() <= 0.2: # 20% sansa da se aktivira
            # Motion detected
            button.button_released_callback() # edge falling, button released
            time.sleep(4)
            button.button_pressed_callback() # edge rising, button pressed
            time.sleep(4)
            #button.button_released_callback() # edge falling, button released
            #time.sleep(10)
            #button.button_pressed_callback() # edge rising, button pressed
        time.sleep(3)