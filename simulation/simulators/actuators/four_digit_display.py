import sys
import threading
import time

def run_display_simulator(callback, stop_event, settings, publish_event):
    def input_listener():
        while not stop_event.is_set():
            val = sys.stdin.readline().strip()
            if len(val) > 0:
                current_value = str(val).rjust(4)[:4]
                callback(current_value, settings, publish_event)

    threading.Thread(target=input_listener, daemon=True).start()

    while not stop_event.is_set():
        time.sleep(0.1)
