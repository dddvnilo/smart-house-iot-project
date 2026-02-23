from devices.sensors.infrared_receiver import Infrared_receiver, run_infrared_receiver_loop
from simulators.sensors.infrared_receiver import Infrared_receiver_simulator, run_infrared_receiver_simulator
import threading
import time
import paho.mqtt.publish as publish
from broker_settings import HOSTNAME, PORT
import json

ir_batch = []
publish_data_counter = 0
publish_data_limit = 5
counter_lock = threading.Lock()

def publisher_task(event, ir_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_ir_batch = ir_batch.copy()
            publish_data_counter = 0
            ir_batch.clear()
        publish.multiple(local_ir_batch, hostname=HOSTNAME, port=PORT)
        print(f'published {publish_data_limit} ir values')
        event.clear()

publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, ir_batch,))
publisher_thread.daemon = True
publisher_thread.start()

def ir_callback(button, settings, publish_event):
    global publish_data_counter, publish_data_limit

    t = time.localtime()
    print("\n"+"="*20)
    print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    print(f"IR: Button pressed: {button}")

    button_pressed_payload = {
        "measurement": "ButtonPressed",
        "simulated": settings['simulated'],
        "runs_on": settings["runs_on"],
        "name": settings["name"],
        "timestamp": time.time(),
        "value": button
    }

    with counter_lock:
        ir_batch.append(('home/bedroom/infrared_receiver', json.dumps(button_pressed_payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()

def run_ir(settings, threads, stop_event):
    ir = None

    if settings['simulated']:
        print("Starting IR simulator")
        ir = Infrared_receiver_simulator(settings=settings, publish_event=publish_event, callback=ir_callback)
        ir_thread = threading.Thread(target = run_infrared_receiver_simulator, args=(ir, stop_event))
        ir_thread.start()
        threads.append(ir_thread)
        print("IR sumilator started")
    else:
        print("Starting IR loop")
        ir = Infrared_receiver(settings=settings, publish_event=publish_event, callback=ir_callback)
        ir_thread = threading.Thread(target = run_infrared_receiver_loop, args=(ir, stop_event))
        ir_thread.start()
        threads.append(ir_thread)
        print("IR loop started")
    
    return ir