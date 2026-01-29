import random
import time

def run_pir_simulator(callback, stop_event, publish_event, settings):
    while not stop_event.is_set():
        if random.random() <= 0.2: # 20% sansa da se aktivira
            # Motion detected
            callback(True, settings, publish_event) # edge rising
            time.sleep(1)
            callback(False, settings, publish_event) # edge falling
        time.sleep(5)