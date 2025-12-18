import random
import time

def run_pir_simulator(callback, stop_event):
    while not stop_event.is_set():
        if random.random() <= 0.2: # 20% sansa da se aktivira
            # Motion detected
            callback(True)
            time.sleep(1)
            callback(False)
        time.sleep(0.5)