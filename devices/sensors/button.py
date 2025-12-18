try:
    import RPi.GPIO as GPIO
    from utils import PULL_MAP
except:
    pass
import time


class Button(object):
    def __init__(self,pin, pmode, callback):
        self.pin = pin
        self.pmode = PULL_MAP[pmode]
        self.callback = callback
        GPIO.setup(self.pin, GPIO.IN, pull_up_down = pmode)
        if(pmode == GPIO.PUD_UP):
            GPIO.add_event_detect(self.pin, GPIO.RISING, callback = self.button_released_callback, bouncetime = 100)
            GPIO.add_event_detect(self.pin,GPIO.FALLING,callback= self.button_pressed_callback, bouncetime=100)
        elif(pmode == GPIO.PUD_DOWN):
            GPIO.add_event_detect(self.pin, GPIO.FALLING, callback = self.button_released_callback, bouncetime = 100)
            GPIO.add_event_detect(self.pin,GPIO.RISING,callback= self.button_pressed_callback, bouncetime=100)
        
    def button_pressed_callback(self):
        self.callback(False)

    def button_released_callback(self):
        self.callback(True)

def run_button_loop(ds, stop_event):
    while True:
        if stop_event.is_set():
            break