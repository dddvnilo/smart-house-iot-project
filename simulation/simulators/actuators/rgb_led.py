import sys
import threading
import time

def run_rgb_simulator(callback, stop_event, settings, publish_event):
    def input_listener():
        while not stop_event.is_set():
            key = sys.stdin.readline().strip().lower()
            if key == '1':
                callback("RED", settings, publish_event)
            elif key == '2':
                callback("GREEN", settings, publish_event)
            elif key == '3':
                callback("BLUE", settings, publish_event)
            elif key == '4':
                callback("YELLOW", settings, publish_event)
            elif key == '5':
                callback("PURPLE", settings, publish_event)
            elif key == '6':
                callback("LIGHT_BLUE", settings, publish_event)
            elif key == '7':
                callback("WHITE", settings, publish_event)
            elif key == '8':
                callback("OFF", settings, publish_event)


    threading.Thread(target=input_listener, daemon=True).start()

    while not stop_event.is_set():
        time.sleep(0.1)
