from devices.actuators.rgb_led import RGB_LED, run_rgb_loop
from simulators.actuators.rgb_led import RGB_LED_simulator, run_rgb_simulator
import threading
import time
import json
import paho.mqtt.publish as publish
from broker_settings import HOSTNAME, PORT

rgb_led_batch = []
publish_data_counter = 0
publish_data_limit = 1
counter_lock = threading.Lock()

def publisher_task(event, rgb_led_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_rgb_led_batch = rgb_led_batch.copy()
            publish_data_counter = 0
            rgb_led_batch.clear()
        publish.multiple(local_rgb_led_batch, hostname=HOSTNAME, port=PORT)
        print(f'published {publish_data_limit} rgb led values')
        event.clear()

publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, rgb_led_batch,))
publisher_thread.daemon = True
publisher_thread.start()

def brgb_callback(color, settings, publish_event):
    global publish_data_counter, publish_data_limit

    t = time.localtime()
    print("\n"+"="*20)
    print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    # state kao True/False
    print("BRGB: Current color: " + color)

    color_payload = {
        "measurement": "Color",
        "simulated": settings['simulated'],
        "runs_on": settings["runs_on"],
        "name": settings["name"],
        "timestamp": time.time(),
        "value": color
    }

    with counter_lock:
        rgb_led_batch.append(('home/bedroom/rgb_led', json.dumps(color_payload), 0, False))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()

def run_brgb(settings, threads, stop_event):
    brgb = None

    if settings['simulated']:
        print("Starting BRGB simulator")
        brgb = RGB_LED_simulator(settings=settings, publish_event=publish_event, callback=brgb_callback)
        brgb_thread = threading.Thread(target = run_rgb_simulator, args=(brgb, stop_event))
        brgb_thread.start()
        threads.append(brgb_thread)
        print("DL sumilator started")
    else:
        print("Starting BRGB loop")
        brgb = RGB_LED(settings=settings, publish_event=publish_event, callback=brgb_callback)
        brgb_thread = threading.Thread(target = run_rgb_loop, args=(brgb, stop_event))
        brgb_thread.start()
        threads.append(brgb_thread)
        print("BRGB loop started")

    return brgb