from simulators.actuators.buzzer import run_buzzer_simulator
import threading
import time
import json
import paho.mqtt.publish as publish
from broker_settings import HOSTNAME, PORT
from devices.actuators.buzzer import Buzzer, run_buzz_loop

buzz_batch = []
publish_data_counter = 0
publish_data_limit = 1
counter_lock = threading.Lock()

def publisher_task(event, buzz_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_buzz_batch = buzz_batch.copy()
            publish_data_counter = 0
            buzz_batch.clear()
        publish.multiple(local_buzz_batch, hostname=HOSTNAME, port=PORT)
        print(f'published {publish_data_limit} buzzer values')
        event.clear()

publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, buzz_batch,))
publisher_thread.daemon = True
publisher_thread.start()

def db_callback(settings, publish_event):
    global publish_data_counter, publish_data_limit

    t = time.localtime()
    print("\n"+"="*20)
    print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    print("DB: Buzz buzz")

    buzzer_activated_payload = {
        "measurement": "BuzzerActivated",
        "simulated": settings['simulated'],
        "runs_on": settings["runs_on"],
        "name": settings["name"],
        "timestamp": time.time(),
        "value": True # TODO: promeniti na nesto bolje posto da se stavi samo timestamp je bzvz na grafani a i vec imamo timestamp
    }

    with counter_lock:
        buzz_batch.append(('home/front-door/door_buzzer', json.dumps(buzzer_activated_payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()

def run_db(settings, threads, stop_event):
    if settings['simulated']:
        print("Starting DB simulator")
        db_thread = threading.Thread(target = run_buzzer_simulator, args=(db_callback, stop_event, settings, publish_event))
        db_thread.start()
        threads.append(db_thread)
        print("DB sumilator started")
    else:
        print("Starting DB loop")
        db = Buzzer(settings=settings, publish_event=publish_event, callback=db_callback)
        db_thread = threading.Thread(target = run_buzz_loop, args=(db, stop_event))
        db_thread.start()
        threads.append(db_thread)
        print("DB loop started")