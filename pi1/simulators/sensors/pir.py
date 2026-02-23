import random
import time

class PIR_simulator(object):
    def __init__(self,settings,callback, publish_event):
        self.pin = settings["pin"]
        self.callback = callback
        self.settings = settings
        self.publish_event = publish_event

    def motion_detected(self, channel=0):
        self.callback(True, self.settings, self.publish_event)

    def no_motion(self, channel=0):
        self.callback(False, self.settings, self.publish_event)

def run_pir_simulator(pir, stop_event):
    while not stop_event.is_set():
        if random.random() <= 1: # 20% sansa da se aktivira
            # Motion detected
            pir.motion_detected() # edge rising
            time.sleep(2)
            pir.no_motion() # edge falling
        time.sleep(5)