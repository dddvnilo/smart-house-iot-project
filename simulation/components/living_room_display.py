from simulators.actuators.lcd import run_lcd_simulator
import threading
import time
from devices.actuators.lcd import LCD, run_lcd_loop
import paho.mqtt.publish as publish
from broker_settings import HOSTNAME, PORT
import json

lcd_batch = []
publish_data_counter = 0
publish_data_limit = 1
counter_lock = threading.Lock()

def publisher_task(event, lcd_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_lcd_batch = lcd_batch.copy()
            publish_data_counter = 0
            lcd_batch.clear()
        publish.multiple(local_lcd_batch, hostname=HOSTNAME, port=PORT)
        print(f'published {publish_data_limit} lcd values')
        event.clear()

publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, lcd_batch,))
publisher_thread.daemon = True
publisher_thread.start()

def lcd_callback(lcd_print, settings, publish_event):
    global publish_data_counter, publish_data_limit

    t = time.localtime()
    print("\n"+"="*20)
    print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    print("LCD: displayed " + lcd_print)

    shown_on_lcd_payload = {
        "measurement": "ShownOnLCD",
        "simulated": settings['simulated'],
        "runs_on": settings["runs_on"],
        "name": settings["name"],
        "timestamp": time.time(),
        "value": lcd_print
    }

    with counter_lock:
        lcd_batch.append(('home/living-room/lcd', json.dumps(shown_on_lcd_payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()

def run_lcd(settings, threads, stop_event):
    if settings['simulated']:
        print("Starting LCD simulator")
        lcd_thread = threading.Thread(target = run_lcd_simulator, args=(lcd_callback, stop_event, settings, publish_event))
        lcd_thread.start()
        threads.append(lcd_thread)
        print("LCD simulator started")
    else:
        print("Starting LCD loop")
        lcd = LCD(settings=settings, publish_event=publish_event, callback=lcd_callback)
        lcd_thread = threading.Thread(target = run_lcd_loop, args=(lcd, stop_event))
        lcd_thread.start()
        threads.append(lcd_thread)
        print("LCD loop started")
