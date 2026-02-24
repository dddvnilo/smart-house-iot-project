import time
import threading
from simulators.sensors.button import Button_simulator, run_button_simulator
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
        print(f'published {publish_data_limit} btn values')
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
        print("BTN: Button is released!")
    else:
        print("BTN: Button is pressed!")

    is_unlocked_payload = {
        "measurement": "IsButtonPressed",
        "simulated": settings['simulated'],
        "runs_on": settings["runs_on"],
        "name": settings["name"],
        "timestamp": time.time(),
        "value": unlocked
    }

    with counter_lock:
        ds_batch.append(('home/kitchen/button', json.dumps(is_unlocked_payload), 0, False))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()

def run_btn(settings, threads, stop_event):
    ds1 = None

    if settings['simulated']:
        print("Starting BTN simulator")
        ds1 = Button_simulator(settings=settings, publish_event=publish_event, callback=ds1_callback)
        ds1_thread = threading.Thread(target = run_button_simulator, args=(ds1, stop_event))
        ds1_thread.start()
        threads.append(ds1_thread)
        print("BTN sumilator started")
    else:
        print("Starting BTN loop")
        ds1 = Button(settings=settings, publish_event=publish_event, callback=ds1_callback)
        ds1_thread = threading.Thread(target = run_button_loop, args=(ds1, stop_event))
        ds1_thread.start()
        threads.append(ds1_thread)
        print("BTN loop started")

    return ds1

