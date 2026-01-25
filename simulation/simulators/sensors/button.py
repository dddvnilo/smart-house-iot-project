import random
import time

def run_button_simulator(callback, stop_event):
    while not stop_event.is_set():
        if random.random() <= 0.2: # 20% sansa da se aktivira
            # Motion detected
            callback(True) # edge falling, button released
            time.sleep(1)
            callback(False) # edge rising, button pressed
        time.sleep(5)