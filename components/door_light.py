from simulators.actuators.led import run_led_simulator
import threading
import time
from devices.actuators.led import LED, run_led_loop

def dl_callback(state):
    t = time.localtime()
    print("\n"+"="*20)
    print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    # state kao True/False
    if state:
        print("DL: Door Light turned ON")
    else:
        print("DL: Door Light turned OFF")

def run_dl(settings, threads, stop_event):
    if settings['simulated']:
        print("Starting DL simulator")
        dl_thread = threading.Thread(target = run_led_simulator, args=(dl_callback, stop_event))
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