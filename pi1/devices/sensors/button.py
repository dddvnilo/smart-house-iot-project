try:
    import RPi.GPIO as GPIO
    from utils import PULL_MAP
except:
    pass
import time


class Button(object):
    def __init__(self,settings,callback, publish_event):
        self.pin = settings["pin"]
        self.pmode = PULL_MAP[settings["pull"]]
        self.callback = callback
        self.settings = settings
        self.publish_event = publish_event
        GPIO.setup(self.pin, GPIO.IN, pull_up_down = self.pmode)
        
    def button_pressed_callback(self):
        self.callback(False, self.settings, self.publish_event)

    def button_released_callback(self):
        self.callback(True, self.settings, self.publish_event)

    def determine_callback(self, channel):
        state = GPIO.input(self.pin)

        if self.pmode == GPIO.PUD_UP:
            pressed = (state == GPIO.LOW)
        else:
            pressed = (state == GPIO.HIGH)

        if pressed:
            self.button_pressed_callback()
        else:
            self.button_released_callback()


    def start_detecting(self):
        GPIO.add_event_detect(
            self.pin,
            GPIO.BOTH,
            callback=self.determine_callback,
            bouncetime=120
        )

def run_button_loop(button, stop_event):
    button.start_detecting()
    while True:
        if stop_event.is_set():
            break