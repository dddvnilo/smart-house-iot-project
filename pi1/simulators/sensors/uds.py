import random
import time

class UDS_simulator(object):
    def __init__(self,settings,callback, publish_event):
        self.callback = callback
        self.trig_pin = settings["trig_pin"]
        self.echo_pin = settings["echo_pin"]
        self.scan_delay = settings["scan_delay"]
        self.settings = settings
        self.publish_event = publish_event

    def send_distance(self, distance):
        self.callback(distance, self.settings, self.publish_event)

def run_uds_simulator(uds, stop_event):
    min_distance=1
    max_distance=20000
    step = 1.5
    distance = 20000
    while not stop_event.is_set():
        # nasumicna udaljenost
        distance += step
        if(distance >= max_distance):
            step = -1.5
        if(distance <= min_distance):
            step = 1.5
        uds.send_distance(distance)
        time.sleep(uds.scan_delay)