import time
import threading
from simulators.sensors.button import run_button_simulator
from devices.sensors.button import Button, run_button_loop

def ds1_callback(unlocked):
    t = time.localtime()
    print("\n"+"="*20)
    print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    if unlocked:
        print("DS1: Door is unlocked!")
    else:
        print("DS1: Door is locked!")

def run_ds1(settings, threads, stop_event):
    if settings['simulated']:
        print("Starting DS1 simulator")
        ds1_thread = threading.Thread(target = run_button_simulator, args=(ds1_callback, stop_event))
        ds1_thread.start()
        threads.append(ds1_thread)
        print("DS1 sumilator started")
    else:
        print("Starting DS1 loop")
        ds1 = Button(settings["pin"], settings["pull"],callback=ds1_callback)
        ds1_thread = threading.Thread(target = run_button_loop, args=(ds1, stop_event))
        ds1_thread.start()
        threads.append(ds1_thread)
        print("DS1 loop started")

