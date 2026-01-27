from simulators.sensors.uds import run_uds_simulator
import threading
import time
from devices.sensors.uds import UDS, run_uds_loop
import paho.mqtt.publish as publish
from broker_settings import HOSTNAME, PORT
import json

uds_batch = []
publish_data_counter = 0
publish_data_limit = 10
counter_lock = threading.Lock()

def publisher_task(event, uds_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_uds_batch = uds_batch.copy()
            publish_data_counter = 0
            uds_batch.clear()
        publish.multiple(local_uds_batch, hostname=HOSTNAME, port=PORT)
        print(f'published {publish_data_limit} uds values')
        event.clear()

publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, uds_batch,))
publisher_thread.daemon = True
publisher_thread.start()

def dus1_callback(distance, settings, publish_event):
    global publish_data_counter, publish_data_limit

    t = time.localtime()
    print("\n"+"="*20)
    print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    print(f"DUS1: Distance measured: {distance:.2f} cm")

    dist_payload = {
        "measurement": "Distance",
        "simulated": settings['simulated'],
        "runs_on": settings["runs_on"],
        "name": settings["name"],
        "value": distance
    }

    with counter_lock:
        uds_batch.append(('Distance', json.dumps(dist_payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()

def run_dus1(settings, threads, stop_event):
    if settings['simulated']:
        print("Starting DUS1 simulator")
        dus_thread = threading.Thread(target = run_uds_simulator, args=(dus1_callback, stop_event, publish_event, settings))
        dus_thread.start()
        threads.append(dus_thread)
        print("DUS1 sumilator started")
    else:
        print("Starting DUS1 loop")
        dus = UDS(trig_pin=settings["trig_pin"], echo_pin=settings["echo_pin"], scan_delay=settings["scan_delay"], callback=dus1_callback)
        dus_thread = threading.Thread(target = run_uds_loop, args=(dus, stop_event))
        dus_thread.start()
        threads.append(dus_thread)
        print("DUS1 loop started")