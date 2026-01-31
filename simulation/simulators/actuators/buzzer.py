import sys
import threading
import time

def run_buzzer_simulator(callback, stop_event, settings, publish_event):
    def input_listener():
        while not stop_event.is_set():
            key = sys.stdin.readline().strip().lower()
            if key == 'b':
                callback(settings, publish_event)

    threading.Thread(target=input_listener, daemon=True).start()

    while not stop_event.is_set():
        time.sleep(0.1)
