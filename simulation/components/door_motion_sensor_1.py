from simulators.sensors.pir import run_pir_simulator
import time
import threading
from devices.sensors.pir import PIR, run_pir_loop
import paho.mqtt.publish as publish
from broker_settings import HOSTNAME, PORT
import json

dpir_batch = []
publish_data_counter = 0
publish_data_limit = 5
counter_lock = threading.Lock()

def publisher_task(event, dpir_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_dpir__batch = dpir_batch.copy()
            publish_data_counter = 0
            dpir_batch.clear()
        publish.multiple(local_dpir__batch, hostname=HOSTNAME, port=PORT)
        print(f'published {publish_data_limit} dpir values')
        event.clear()

publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, dpir_batch,))
publisher_thread.daemon = True
publisher_thread.start()

def dpir1_callback(motion, settings, publish_event):
    global publish_data_counter, publish_data_limit

    t = time.localtime()
    print("\n"+"="*20)
    print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    if motion:
        print("DPIR1: Motion detected!")
    else:
        print("DPIR1: Motion stopped.")

    motion_payload = {
        "measurement": "MotionDetected",
        "simulated": settings['simulated'],
        "runs_on": settings["runs_on"],
        "name": settings["name"],
        "timestamp": time.time(),
        "value": motion
    }

    with counter_lock:
        dpir_batch.append(('home/front-door/door_motion_sensor', json.dumps(motion_payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()

def run_dpir1(settings, threads, stop_event):
    if settings['simulated']:
        print("Starting DPIR1 simulator")
        dpir1_thread = threading.Thread(target = run_pir_simulator, args=(dpir1_callback, stop_event, publish_event, settings))
        dpir1_thread.start()
        threads.append(dpir1_thread)
        print("DPIR1 sumilator started")
    else:
        print("Starting DPIR1 loop")
        dpir1 = PIR(settings=settings, publish_event=publish_event, callback=dpir1_callback)
        dpir1_thread = threading.Thread(target = run_pir_loop, args=(dpir1, stop_event))
        dpir1_thread.start()
        threads.append(dpir1_thread)
        print("DPIR1 loop started")