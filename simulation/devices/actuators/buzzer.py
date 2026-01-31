try:
    import RPi.GPIO as GPIO
except:
    pass
import time
import threading
import sys


class Buzzer(object):
    def __init__(self, settings, publish_event, callback):
        self.pin = settings['pin']
        self.publish_event = publish_event
        self.callback = callback
        self.settings = settings
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
    

    def buzz(self):
        
        period = 1.0 / self.pitch
        delay = period / 2
        cycles = int(self.duration * self.pitch)

        self.callback(self.settings, self.publish_event)

        for i in range(cycles):
            GPIO.output(self.pin, True)
            time.sleep(delay)
            GPIO.output(self.pin, False)
            time.sleep(delay)

def run_buzz_loop(buzzer, stop_event):
    def input_listener():
        while not stop_event.is_set():
            key = sys.stdin.readline().strip().lower()
            if key == 'b':
                buzzer.buzz()

    threading.Thread(target=input_listener, daemon=True).start()

    while not stop_event.is_set():
        time.sleep(0.1)
            