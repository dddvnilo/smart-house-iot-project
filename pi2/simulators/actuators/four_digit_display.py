import sys
import threading
import time

class FourDigitDisplay_simulator(object):
    def __init__(self, settings, publish_event, callback):
        self.segments = settings["segments"]   # tuple 8 pinova
        self.digits = settings["digits"]       # tuple 4 pinova
        self.publish_event = publish_event
        self.callback = callback
        self.settings = settings
        self.is_blinking = False
        self.current_value = "0000"

        # mapa cifara
        self.num = {
            ' ':(0,0,0,0,0,0,0),
            '0':(1,1,1,1,1,1,0),
            '1':(0,1,1,0,0,0,0),
            '2':(1,1,0,1,1,0,1),
            '3':(1,1,1,1,0,0,1),
            '4':(0,1,1,0,0,1,1),
            '5':(1,0,1,1,0,1,1),
            '6':(1,0,1,1,1,1,1),
            '7':(1,1,1,0,0,0,0),
            '8':(1,1,1,1,1,1,1),
            '9':(1,1,1,1,0,1,1)
        }

    def set_blinking(self,is_blinking):
        with threading.Lock():
            self.is_blinking = is_blinking

    def set_value(self, value):
        with threading.Lock():
            self.current_value = value

    def display(self):
        with threading.Lock():
            display_value = str(self.current_value).rjust(4)[:4]
            should_blink = self.is_blinking
        
        if should_blink:
            display_value += " (blinking)"

        self.callback(display_value, self.settings, self.publish_event)


def run_display_simulator(display, stop_event):
    while not stop_event.is_set():
        display.display()
        time.sleep(1)
