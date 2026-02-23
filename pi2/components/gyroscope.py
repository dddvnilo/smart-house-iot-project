from simulators.sensors.gyroscope import Gyroscope_simulator, run_gsg_simulator
import threading
import time
from devices.sensors.gyroscope import Gyroscope, run_gsg_loop
import paho.mqtt.publish as publish
from broker_settings import HOSTNAME, PORT
import json

gsg_batch = []
publish_data_counter = 0
publish_data_limit = 1
counter_lock = threading.Lock()

def publisher_task(event, gsg_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_gsg_batch = gsg_batch.copy()
            publish_data_counter = 0
            gsg_batch.clear()
        publish.multiple(local_gsg_batch, hostname=HOSTNAME, port=PORT)
        print(f'published {publish_data_limit} gyroscope values')
        event.clear()

publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, gsg_batch,))
publisher_thread.daemon = True
publisher_thread.start()

def gsg_callback(gyroscope_data, settings, publish_event):
    global publish_data_counter, publish_data_limit

    t = time.localtime()
    print("\n"+"="*20)
    print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")

    ax, ay, az = gyroscope_data["accel_g"]
    gx, gy, gz = gyroscope_data["gyro_dps"]
    print(f"""
    GSG: 
    ACCELEROMETER:
    X: {ax:+.2f} g   Y: {ay:+.2f} g   Z: {az:+.2f} g

    GYROSCOPE:
    X: {gx:+.1f} °/s   Y: {gy:+.1f} °/s   Z: {gz:+.1f} °/s
    """)

    acl_payload = {
        "measurement": "Accelerometer",
        "simulated": settings['simulated'],
        "runs_on": settings["runs_on"],
        "name": settings["name"],
        "timestamp": time.time(),

        # fizicke vrednosti
        "value": gyroscope_data["accel_g"],     # [ax_g, ay_g, az_g]
    }

    gsg_payload = {
        "measurement": "Gyroscope",
        "simulated": settings['simulated'],
        "runs_on": settings["runs_on"],
        "name": settings["name"],
        "timestamp": time.time(),

        # fizicke vrednosti
        "value": gyroscope_data["gyro_dps"],   # [gx_dps, gy_dps, gz_dps]
    }

    acl_payload["value"] = f"{ax:+.2f},{ay:+.2f},{az:+.2f}"
    gsg_payload["value"] = f"{gx:+.1f},{gy:+.1f},{gz:+.1f}"

    with counter_lock:
        gsg_batch.append(('home/dining-room/gyroscope', json.dumps(acl_payload), 0, True))
        gsg_batch.append(('home/dining-room/gyroscope', json.dumps(gsg_payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()

def run_gsg(settings, threads, stop_event):
    gyro = None 

    if settings['simulated']:
        print("Starting GSG simulator")
        gyro = Gyroscope_simulator(settings=settings, publish_event=publish_event, callback=gsg_callback)
        gsg_thread = threading.Thread(target = run_gsg_simulator, args=(gyro, stop_event))
        gsg_thread.start()
        threads.append(gsg_thread)
        print("GSG sumilator started")
    else:
        print("Starting GSG loop")
        gyro = Gyroscope(settings=settings, publish_event=publish_event, callback=gsg_callback)
        gsg_thread = threading.Thread(target = run_gsg_loop, args=(gyro, stop_event))
        gsg_thread.start()
        threads.append(gsg_thread)
        print("GSG loop started")

    return gyro