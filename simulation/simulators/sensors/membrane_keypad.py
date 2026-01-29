import random
import time

def run_membrane_keypad_simulator(callback, stop_event, publish_event, settings):
    keys = ['1','2','3','A',
            '4','5','6','B',
            '7','8','9','C',
            '*','0','#','D']

    while not stop_event.is_set():
        if random.random() < 0.2: # 20% sansa da se aktivira
            key = random.choice(keys)
            callback(key, settings, publish_event)
        time.sleep(settings["scan_delay"])