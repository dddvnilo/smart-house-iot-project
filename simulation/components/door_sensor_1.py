import time
import threading
from simulators.sensors.button import run_button_simulator
from devices.sensors.button import Button, run_button_loop
import paho.mqtt.publish as publish
from broker_settings import HOSTNAME, PORT
import json

ds_batch = []
publish_data_counter = 0
publish_data_limit = 1
counter_lock = threading.Lock()

def publisher_task(event, ds_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_ds_batch = ds_batch.copy()
            publish_data_counter = 0
            ds_batch.clear()
        publish.multiple(local_ds_batch, hostname=HOSTNAME, port=PORT)
        print(f'published {publish_data_limit} ds values')
        event.clear()

publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, ds_batch,))
publisher_thread.daemon = True
publisher_thread.start()

def ds1_callback(unlocked, settings, publish_event):
    global publish_data_counter, publish_data_limit

    t = time.localtime()
    print("\n"+"="*20)
    print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    if unlocked:
        print("DS1: Door is unlocked!")
    else:
        print("DS1: Door is locked!")

    is_unlocked_payload = {
        "measurement": "IsUnlocked",
        "simulated": settings['simulated'],
        "runs_on": settings["runs_on"],
        "name": settings["name"],
        "timestamp": time.time(),
        "value": unlocked
    }

    with counter_lock:
        ds_batch.append(('home/front-door/door_sensor', json.dumps(is_unlocked_payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()

def run_ds1(settings, threads, stop_event):
    if settings['simulated']:
        print("Starting DS1 simulator")
        ds1_thread = threading.Thread(target = run_button_simulator, args=(ds1_callback, stop_event, publish_event, settings))
        ds1_thread.start()
        threads.append(ds1_thread)
        print("DS1 sumilator started")
    else:
        print("Starting DS1 loop")
        ds1 = Button(settings=settings, publish_event=publish_event, callback=ds1_callback)
        ds1_thread = threading.Thread(target = run_button_loop, args=(ds1, stop_event))
        ds1_thread.start()
        threads.append(ds1_thread)
        print("DS1 loop started")

