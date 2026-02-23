import time
import random

class DHT_simulator(object):
    def __init__(self, settings, callback, publish_event):
        self.pin = settings["pin"]
        self.settings = settings
        self.scan_delay = settings["scan_delay"]
        self.callback = callback
        self.publish_event = publish_event

    def send_humidity_temperature(self, humidity, temperature):
        self.callback(humidity, temperature, self.settings, self.publish_event)

def generate_values(initial_temp = 25, initial_humidity=20):
      temperature = initial_temp
      humidity = initial_humidity
      while True:
            temperature = temperature + random.randint(-1, 1)
            humidity = humidity + random.randint(-1, 1)
            if humidity < 0:
                  humidity = 0
            if humidity > 100:
                  humidity = 100
            yield humidity, temperature

def run_dht_simulator(dht, stop_event):
        for h, t in generate_values():
            time.sleep(dht.scan_delay)
            dht.send_humidity_temperature(humidity=h, temperature=t)
            if stop_event.is_set():
                  break