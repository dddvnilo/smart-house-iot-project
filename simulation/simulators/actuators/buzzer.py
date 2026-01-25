import keyboard
import time

def run_buzzer_simulator(callback, stop_event):
    while not stop_event.is_set():
        # na b sa tastature aktiviramo buzzer
        if keyboard.is_pressed('b'):
            callback()
            while keyboard.is_pressed('b'):
                time.sleep(0.05)
            time.sleep(0.05)