import time

def run_buzzer_simulator(callback, settings, stop_event):
    while not stop_event.is_set():
        # na b sa tastature aktiviramo buzzer
        key = input("").strip().lower()
        if key == 'b':
            callback(settings['duration'])