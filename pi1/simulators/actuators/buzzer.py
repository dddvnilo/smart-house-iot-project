import sys
import threading
import time

class Buzzer_simulator(object):
    def __init__(self, settings, publish_event, callback):
        self.pin = settings['pin']
        self.publish_event = publish_event
        self.pitch = settings['pitch']
        self.duration = settings['duration']
        self.callback = callback
        self.settings = settings
        self.alarm = False

    def buzz(self):
        self.callback(self.settings, self.publish_event)

    def alarm_buzz(self, alarm):
        with threading.Lock():
            self.alarm = alarm

def run_buzzer_simulator(buzzer, stop_event):
    def input_listener():
        while not stop_event.is_set():
            key = sys.stdin.readline().strip().lower()
            if key == 'b':
                buzzer.buzz()

    threading.Thread(target=input_listener, daemon=True).start()

    while not stop_event.is_set():
        if buzzer.alarm:
            buzzer.buzz()
            time.sleep(2)
        time.sleep(0.1)
