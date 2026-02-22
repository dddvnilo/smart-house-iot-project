try:
    import RPi.GPIO as GPIO
except:
    pass
import time
import threading
import sys


class FourDigitDisplay(object):
    def __init__(self, settings, publish_event, callback):
        self.segments = settings["segments"]   # tuple 8 pinova
        self.digits = settings["digits"]       # tuple 4 pinova
        self.publish_event = publish_event
        self.callback = callback
        self.settings = settings
        self.blink_colon = False
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

        # GPIO setup
        for s in self.segments:
            GPIO.setup(s, GPIO.OUT)
            GPIO.output(s, 0)

        for d in self.digits:
            GPIO.setup(d, GPIO.OUT)
            GPIO.output(d, 1)


    def display(self, value, blink_colon):
        self.current_value = str(value).rjust(4)[:4]
        self.blink_colon = blink_colon
        self.callback(self.current_value, self.settings, self.publish_event)


    def refresh_once(self):
            s = self.current_value

            for digit in range(4):
                # segmenti
                for seg in range(7):
                    GPIO.output(self.segments[seg], self.num[s[digit]][seg])

                # decimal point blink
                if len(self.segments) >= 8:
                    if self.blink_colon and digit == 1:
                        sec = int(time.time()) % 2
                        GPIO.output(self.segments[7], 1 if sec == 0 else 0)
                    else:
                        GPIO.output(self.segments[7], 0)

                GPIO.output(self.digits[digit], 0)
                time.sleep(0.001)
                GPIO.output(self.digits[digit], 1)


def run_display_loop(display, stop_event):
    def input_listener():
        while not stop_event.is_set():
            val = sys.stdin.readline().strip()
            if len(val) > 0:
                display.display(val, blink_colon = True)

    threading.Thread(target=input_listener, daemon=True).start()

    while not stop_event.is_set():
        display.refresh_once()
        time.sleep(0.001)