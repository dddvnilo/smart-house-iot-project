try:
    import RPi.GPIO as GPIO
except:
    pass
import time


class PIR(object):
    def __init__(self,settings,callback, publish_event):
        self.pin = settings["pin"]
        self.callback = callback
        self.settings = settings
        self.publish_event = publish_event

        GPIO.setup(self.pin, GPIO.IN)

    def motion_detected(self, channel):
        self.callback(True, self.settings, self.publish_event)

    def no_motion(self, channel):
        self.callback(False, self.settings, self.publish_event)

    def start_detecting(self):
        GPIO.add_event_detect(self.pin, GPIO.RISING, callback=self.motion_detected)
        GPIO.add_event_detect(self.pin, GPIO.FALLING, callback=self.no_motion)

def run_pir_loop(pir, stop_event):
    pir.start_detecting()
    while True:
        if stop_event.is_set():
            break