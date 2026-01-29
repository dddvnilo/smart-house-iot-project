from simulators.sensors.membrane_keypad import run_membrane_keypad_simulator
import threading
import time
from devices.sensors.membrane_keypad import MembraneKeypad, run_membrane_keypad_loop
import paho.mqtt.publish as publish
from broker_settings import HOSTNAME, PORT
import json

dms_batch = []
publish_data_counter = 0
publish_data_limit = 5
counter_lock = threading.Lock()

def publisher_task(event, dms_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_dms_batch = dms_batch.copy()
            publish_data_counter = 0
            dms_batch.clear()
        publish.multiple(local_dms_batch, hostname=HOSTNAME, port=PORT)
        print(f'published {publish_data_limit} dms values')
        event.clear()

publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, dms_batch,))
publisher_thread.daemon = True
publisher_thread.start()

def dms_callback(key, settings, publish_event):
    global publish_data_counter, publish_data_limit

    t = time.localtime()
    print("\n"+"="*20)
    print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    print(f"DMS: Key pressed: {key}")

    key_pressed_payload = {
        "measurement": "KeyPressed",
        "simulated": settings['simulated'],
        "runs_on": settings["runs_on"],
        "name": settings["name"],
        "timestamp": time.time(),
        "value": key
    }

    with counter_lock:
        dms_batch.append(('home/front-door/door_membrane_switch', json.dumps(key_pressed_payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()

def run_dms(settings, threads, stop_event):
    if settings['simulated']:
        print("Starting DMS simulator")
        dms_thread = threading.Thread(target = run_membrane_keypad_simulator, args=(dms_callback, stop_event, publish_event, settings))
        dms_thread.start()
        threads.append(dms_thread)
        print("DMS sumilator started")
    else:
        print("Starting DMS loop")
        dms = MembraneKeypad(settings=settings, publish_event=publish_event, callback=dms_callback)
        dms_thread = threading.Thread(target = run_membrane_keypad_loop, args=(dms, stop_event))
        dms_thread.start()
        threads.append(dms_thread)
        print("DMS loop started")