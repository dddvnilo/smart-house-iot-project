from simulators.sensors.uds import run_uds_simulator
import threading
import time
from devices.sensors.uds import UDS, run_uds_loop

def dus1_callback(distance):
    t = time.localtime()
    print("\n"+"="*20)
    print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    print(f"DUS1: Distance measured: {distance:.2f} cm")

def run_dus1(settings, threads, stop_event):
    if settings['simulated']:
        print("Starting DUS1 simulator")
        dus_thread = threading.Thread(target = run_uds_simulator, args=(dus1_callback, stop_event, settings['scan_delay']))
        dus_thread.start()
        threads.append(dus_thread)
        print("DUS1 sumilator started")
    else:
        print("Starting DUS1 loop")
        dus = UDS(trig_pin=settings["trig_pin"], echo_pin=settings["echo_pin"], scan_delay=settings["scan_delay"], callback=dus1_callback)
        dus_thread = threading.Thread(target = run_uds_loop, args=(dus, stop_event))
        dus_thread.start()
        threads.append(dus_thread)
        print("DUS1 loop started")