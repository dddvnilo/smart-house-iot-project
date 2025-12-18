try:
    import RPi.GPIO as GPIO
    from utils import PULL_MAP
except:
    pass
import time
import keyboard


class LED(object):
    def __init__(self,pin, callback):
        self.pin = pin
        self.callback = callback
        self.led_state = False

        GPIO.setup(self.pin,GPIO.OUT)

        GPIO.output(18,GPIO.HIGH)
        time.sleep(1)
        GPIO.output(18,GPIO.LOW)
    

    def toggle_led(self):
        self.led_state = not self.led_state
        if self.led_state:
            GPIO.output(self.pin,GPIO.HIGH)
        else:
            GPIO.output(self.pin,GPIO.LOW)
        self.callback(self.led_state)

    def turn_led_on(self):
        self.led_state = True
        GPIO.output(self.pin,GPIO.HIGH)
        self.callback(self.led_state)

    def turn_led_off(self):
        self.led_state = False
        GPIO.output(self.pin,GPIO.LOW)
        self.callback(self.led_state)

def run_led_loop(led, stop_event):
    while True:
        if keyboard.is_pressed('l'):
            led.toggle_led()
            # while keyboard.is_pressed('l'):
            #    time.sleep(0.05)