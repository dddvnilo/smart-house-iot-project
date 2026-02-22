import sys
import threading
import time


class LED_simulator(object):
    def __init__(self, settings, publish_event, callback):
        self.pin = settings['pin']
        self.settings = settings
        self.publish_event = publish_event
        self.callback = callback
        self.led_state = False
        self.motion_light = False

    def toggle_led(self):
        self.led_state = not self.led_state
        self.callback(self.led_state, self.settings, self.publish_event)

    def turn_led_on(self):
        self.led_state = True
        self.callback(self.led_state, self.settings, self.publish_event)

    def turn_led_off(self):
        self.led_state = False
        self.callback(self.led_state, self.settings, self.publish_event)

    def turn_led_on_for_ten_seconds(self):
        with threading.Lock():
            self.motion_light = True

def run_led_simulator(led, stop_event):
    def input_listener():
        while not stop_event.is_set():
            key = sys.stdin.readline().strip().lower()
            if key == 'l':
                led.toggle_led()

    threading.Thread(target=input_listener, daemon=True).start()

    while not stop_event.is_set():
        if led.motion_light:
            led.turn_led_on()
            time.sleep(10)
            led.turn_led_off()
            with threading.Lock():
                led.motion_light = False
        time.sleep(0.1)
