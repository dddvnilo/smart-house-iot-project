try:
    import RPi.GPIO as GPIO
except:
    pass
import time
import threading
import sys


class RGB_LED(object):
    def __init__(self, settings, publish_event, callback):
        self.red_pin = settings['red_pin']
        self.green_pin = settings['green_pin']
        self.blue_pin = settings['blue_pin']

        self.settings = settings
        self.publish_event = publish_event
        self.callback = callback

        GPIO.setwarnings(False)

        GPIO.setmode(GPIO.BCM)

        #set pins as outputs
        GPIO.setup(self.red_pin, GPIO.OUT)
        GPIO.setup(self.green_pin, GPIO.OUT)
        GPIO.setup(self.blue_pin, GPIO.OUT)
    

    def turn_off(self):
        GPIO.output(self.red_pin, GPIO.LOW)
        GPIO.output(self.green_pin, GPIO.LOW)
        GPIO.output(self.blue_pin, GPIO.LOW)
        self.callback("OFF", self.settings, self.publish_event)

    
    def white(self):
        GPIO.output(self.red_pin, GPIO.HIGH)
        GPIO.output(self.green_pin, GPIO.HIGH)
        GPIO.output(self.blue_pin, GPIO.HIGH)
        self.callback("WHITE", self.settings, self.publish_event)

        
    def red(self):
        GPIO.output(self.red_pin, GPIO.HIGH)
        GPIO.output(self.green_pin, GPIO.LOW)
        GPIO.output(self.blue_pin, GPIO.LOW)
        self.callback("RED", self.settings, self.publish_event)

    def green(self):
        GPIO.output(self.red_pin, GPIO.LOW)
        GPIO.output(self.green_pin, GPIO.HIGH)
        GPIO.output(self.blue_pin, GPIO.LOW)
        self.callback("GREEN", self.settings, self.publish_event)
        
    def blue(self):
        GPIO.output(self.red_pin, GPIO.LOW)
        GPIO.output(self.green_pin, GPIO.LOW)
        GPIO.output(self.blue_pin, GPIO.HIGH)
        self.callback("BLUE", self.settings, self.publish_event)
        
    def yellow(self):
        GPIO.output(self.red_pin, GPIO.HIGH)
        GPIO.output(self.green_pin, GPIO.HIGH)
        GPIO.output(self.blue_pin, GPIO.LOW)
        self.callback("YELLOW", self.settings, self.publish_event)
        
    def purple(self):
        GPIO.output(self.red_pin, GPIO.HIGH)
        GPIO.output(self.green_pin, GPIO.LOW)
        GPIO.output(self.blue_pin, GPIO.HIGH)
        self.callback("PURPLE", self.settings, self.publish_event)
        
    def light_blue(self):
        GPIO.output(self.red_pin, GPIO.LOW)
        GPIO.output(self.green_pin, GPIO.HIGH)
        GPIO.output(self.blue_pin, GPIO.HIGH)
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

def run_rgb_loop(rgb, stop_event):
    while not stop_event.is_set():
        time.sleep(0.1)