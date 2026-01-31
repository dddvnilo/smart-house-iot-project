from simulators.actuators.led import run_led_simulator
import threading
import time
import json
import paho.mqtt.publish as publish
from broker_settings import HOSTNAME, PORT
from devices.actuators.led import LED, run_led_loop

led_batch = []
publish_data_counter = 0
publish_data_limit = 1
counter_lock = threading.Lock()

def publisher_task(event, led_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_led_batch = led_batch.copy()
            publish_data_counter = 0
            led_batch.clear()
        publish.multiple(local_led_batch, hostname=HOSTNAME, port=PORT)
        print(f'published {publish_data_limit} led values')
        event.clear()

publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, led_batch,))
publisher_thread.daemon = True
publisher_thread.start()

def dl_callback(state, settings, publish_event):
    global publish_data_counter, publish_data_limit

    t = time.localtime()
    print("\n"+"="*20)
    print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    # state kao True/False
    if state:
        print("DL: Door Light turned ON")
    else:
        print("DL: Door Light turned OFF")

    is_light_on_payload = {
        "measurement": "IsLightOn",
        "simulated": settings['simulated'],
        "runs_on": settings["runs_on"],
        "name": settings["name"],
        "timestamp": time.time(),
        "value": state
    }

    with counter_lock:
        led_batch.append(('home/front-door/door_light', json.dumps(is_light_on_payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()

def run_dl(settings, threads, stop_event):
    if settings['simulated']:
        print("Starting DL simulator")
        dl_thread = threading.Thread(target = run_led_simulator, args=(dl_callback, stop_event, settings, publish_event))
        dl_thread.start()
        threads.append(dl_thread)
        print("DL sumilator started")
    else:
        print("Starting DL loop")
        dl = LED(settings["pin"], callback=dl_callback)
        dl_thread = threading.Thread(target = run_led_loop, args=(dl, stop_event))
        dl_thread.start()
        threads.append(dl_thread)
        print("DL loop started")