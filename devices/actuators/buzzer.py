try:
    import RPi.GPIO as GPIO
except:
    pass
import time
import keyboard


class Buzzer(object):
    def __init__(self,pin, pitch, duration, callback):
        self.pin = pin
        self.callback = callback
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
    

    def buzz(self):
        
        period = 1.0 / self.pitch
        delay = period / 2
        cycles = int(self.duration * self.pitch)

        self.callback(self.duration)
        
        for i in range(cycles):
            GPIO.output(self.pin, True)
            time.sleep(delay)
            GPIO.output(self.pin, False)
            time.sleep(delay)


def run_buzz_loop(buzzer, stop_event):
    while True:
        if stop_event.is_set():
            break
        if keyboard.is_pressed('b'):
            buzzer.buzz()
            