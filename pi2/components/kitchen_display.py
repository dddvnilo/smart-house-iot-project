from simulators.actuators.four_digit_display import FourDigitDisplay_simulator, run_display_simulator
import threading
import time
import json
import paho.mqtt.publish as publish
from broker_settings import HOSTNAME, PORT
from devices.actuators.four_digit_display import FourDigitDisplay, run_display_loop

display_batch = []
publish_data_counter = 0
publish_data_limit = 1
counter_lock = threading.Lock()

def publisher_task(event, display_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_display_batch = display_batch.copy()
            publish_data_counter = 0
            display_batch.clear()
        publish.multiple(local_display_batch, hostname=HOSTNAME, port=PORT)
        print(f'published {publish_data_limit} display values')
        event.clear()

publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, display_batch,))
publisher_thread.daemon = True
publisher_thread.start()

def display_callback(value, settings, publish_event):
    global publish_data_counter, publish_data_limit

    t = time.localtime()
    print("\n"+"="*20)
    print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    print("4SD: Display showing " + value)

    shown_on_display_payload = {
        "measurement": "ShownOnDisplay",
        "simulated": settings['simulated'],
        "runs_on": settings["runs_on"],
        "name": settings["name"],
        "timestamp": time.time(),
        "value": value
    }

    with counter_lock:
        display_batch.append(('home/kitchen/display', json.dumps(shown_on_display_payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()

def run_4sd(settings, threads, stop_event):
    display = None

    if settings['simulated']:
        print("Starting 4SD simulator")
        display = FourDigitDisplay_simulator(settings=settings, publish_event=publish_event, callback=display_callback)
        display_thread = threading.Thread(target = run_display_simulator, args=(display, stop_event))
        display_thread.start()
        threads.append(display_thread)
        print("4SD sumilator started")
    else:
        print("Starting 4SD loop")
        display = FourDigitDisplay(settings=settings, publish_event=publish_event, callback=display_callback)
        display_thread = threading.Thread(target = run_display_loop, args=(display, stop_event))
        display_thread.start()
        threads.append(display_thread)
        print("4SD loop started")