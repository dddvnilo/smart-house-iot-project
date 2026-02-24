from simulators.sensors.dht import DHT_simulator, run_dht_simulator
import threading
import time
from devices.sensors.dht import DHT, run_dht_loop
import paho.mqtt.publish as publish
from broker_settings import HOSTNAME, PORT
import json

dht_batch = []
publish_data_counter = 0
publish_data_limit = 2
counter_lock = threading.Lock()

def publisher_task(event, dht_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_dht_batch = dht_batch.copy()
            publish_data_counter = 0
            dht_batch.clear()
        publish.multiple(local_dht_batch, hostname=HOSTNAME, port=PORT)
        print(f'published {publish_data_limit} dht values')
        event.clear()

publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, dht_batch,))
publisher_thread.daemon = True
publisher_thread.start()

def dht1_callback(temperature, humidity, settings, publish_event):
    global publish_data_counter, publish_data_limit

    t = time.localtime()
    print("\n"+"="*20)
    print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    print(f"DHT1: Temperature measured: {temperature:.2f}°C")
    print(f"DHT1: Humidity measured: {humidity:.2f}%")

    temp_payload = {
        "measurement": "Temperature",
        "simulated": settings['simulated'],
        "runs_on": settings["runs_on"],
        "name": settings["name"],
        "timestamp": time.time(),
        "value": temperature
    }

    humid_payload = {
        "measurement": "Humidity",
        "simulated": settings['simulated'],
        "runs_on": settings["runs_on"],
        "name": settings["name"],
        "timestamp": time.time(),
        "value": humidity
    }

    with counter_lock:
        # TODO: nzm jel ovo problem
        dht_batch.append(('home/bedroom/dht', json.dumps(temp_payload), 0, False))
        dht_batch.append(('home/bedroom/dht', json.dumps(humid_payload), 0, False))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()

def run_dht1(settings, threads, stop_event):
    dht = None

    if settings['simulated']:
        print("Starting DHT1 simulator")
        dht = DHT_simulator(settings=settings, publish_event=publish_event, callback=dht1_callback)
        dht_thread = threading.Thread(target = run_dht_simulator, args=(dht, stop_event))
        dht_thread.start()
        threads.append(dht_thread)
        print("DHT1 sumilator started")
    else:
        print("Starting DHT1 loop")
        dht = DHT(settings=settings, publish_event=publish_event, callback=dht1_callback)
        dht_thread = threading.Thread(target = run_dht_loop, args=(dht, stop_event))
        dht_thread.start()
        threads.append(dht_thread)
        print("DHT1 loop started")

    return dht