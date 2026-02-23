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

def run_rgb_simulator(rgb, stop_event):
    def input_listener():
        while not stop_event.is_set():
            key = sys.stdin.readline().strip().lower()
            if key == '1':
                rgb.red()
            elif key == '2':
                rgb.green()
            elif key == '3':
                rgb.blue()
            elif key == '4':
                rgb.yellow()
            elif key == '5':
                rgb.purple()
            elif key == '6':
                rgb.light_blue()
            elif key == '7':
                rgb.white()
            elif key == '8':
                rgb.turn_off()


    threading.Thread(target=input_listener, daemon=True).start()

    while not stop_event.is_set():
        time.sleep(0.1)
