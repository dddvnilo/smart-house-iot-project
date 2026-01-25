import random
import time

def run_uds_simulator(callback, stop_event, delay, min_distance=5, max_distance=100):
    while not stop_event.is_set():
        # nasumicna udaljenost
        distance = random.uniform(min_distance, max_distance)
        callback(distance)
        time.sleep(delay)