import keyboard
import time

def run_led_simulator(callback, stop_event):
    led_state = False  # inicijalno LED OFF
    while not stop_event.is_set():
        # na l sa tastature aktiviramo led
        if keyboard.is_pressed('l'):
            led_state = not led_state
            callback(led_state)
            while keyboard.is_pressed('l'):
                time.sleep(0.05)
            time.sleep(0.05)