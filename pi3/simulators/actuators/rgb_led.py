import sys
import threading
import time

class RGB_LED_simulator(object):
    def __init__(self, settings, publish_event, callback):
        self.red_pin = settings['red_pin']
        self.green_pin = settings['green_pin']
        self.blue_pin = settings['blue_pin']

        self.settings = settings
        self.publish_event = publish_event
        self.callback = callback

    def turn_off(self):
        self.callback("OFF", self.settings, self.publish_event)

    
    def white(self):
        self.callback("WHITE", self.settings, self.publish_event)

        
    def red(self):
        self.callback("RED", self.settings, self.publish_event)

    def green(self):
        self.callback("GREEN", self.settings, self.publish_event)
        
    def blue(self):
        self.callback("BLUE", self.settings, self.publish_event)
        
    def yellow(self):
        self.callback("YELLOW", self.settings, self.publish_event)
        
    def purple(self):
        self.callback("PURPLE", self.settings, self.publish_event)
        
    def light_blue(self):
        self.callback("LIGHT_BLUE", self.settings, self.publish_event)

    def led_input(self, key):
        if key == '1':
            self.red()
        elif key == '2':
            self.green()
        elif key == '3':
            self.blue()
        elif key == '4':
            self.yellow()
        elif key == '5':
            self.purple()
        elif key == '6':
            self.light_blue()
        elif key == '7':
            self.white()
        elif key == '8':
            self.turn_off()

def run_rgb_simulator(rgb, stop_event):
    while not stop_event.is_set():
        time.sleep(0.1)
