import time
import random

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

def run_gsg_simulator(callback, stop_event, publish_event, settings):
    for sensor_data in generate_gyroscope_values():
        time.sleep(settings.get("scan_delay", 0.1))
        callback(sensor_data, settings=settings, publish_event=publish_event)
        if stop_event.is_set():
            break