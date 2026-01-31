import sys
import threading
import time

def run_led_simulator(callback, stop_event, settings, publish_event):
    led_state = False

    def input_listener():
        nonlocal led_state
        while not stop_event.is_set():
            key = sys.stdin.readline().strip().lower()
            if key == 'l':
                led_state = not led_state
                callback(led_state, settings, publish_event)

    threading.Thread(target=input_listener, daemon=True).start()

    while not stop_event.is_set():
        time.sleep(0.1)
