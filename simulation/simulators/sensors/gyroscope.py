import time
import random

class Gyroscope_simulator(object):
    def __init__(self, settings, callback, publish_event):
        self.settings = settings
        self.callback = callback
        self.publish_event = publish_event
        self.scan_delay = settings.get("scan_delay", 0.1)

    def send_gyro_data(self, data):
        self.callback(data, self.settings, self.publish_event)


def generate_gyroscope_values():
    while True:
        # simulacija akcelerometra u g
        ax = random.uniform(-1.0, 1.0)
        ay = random.uniform(-1.0, 1.0)
        az = random.uniform(-1.0, 1.0)

        # simulacija giroskopa u °/s
        gx = random.uniform(-180, 180)
        gy = random.uniform(-180, 180)
        gz = random.uniform(-180, 180)

        # raw vrednosti
        accel_raw = [int(a * 16384) for a in (ax, ay, az)]
        gyro_raw = [int(g * 131) for g in (gx, gy, gz)]

        yield {
            "accel_raw": accel_raw,
            "gyro_raw": gyro_raw,
            "accel_g": [ax, ay, az],
            "gyro_dps": [gx, gy, gz]
        }

def run_gsg_simulator(gyro, stop_event):
    for sensor_data in generate_gyroscope_values():
        time.sleep(gyro.scan_delay)
        gyro.send_gyro_data(sensor_data)
        if stop_event.is_set():
            break