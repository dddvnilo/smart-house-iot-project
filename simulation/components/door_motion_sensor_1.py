from simulators.sensors.pir import run_pir_simulator
import time
import threading
from devices.sensors.pir import PIR, run_pir_loop

def dpir1_callback(motion):
    t = time.localtime()
    print("\n"+"="*20)
    print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    if motion:
        print("DPIR1: Motion detected!")
    else:
        print("DPIR1: Motion stopped.")

def run_dpir1(settings, threads, stop_event):
    if settings['simulated']:
        print("Starting DPIR1 simulator")
        dpir1_thread = threading.Thread(target = run_pir_simulator, args=(dpir1_callback, stop_event))
        dpir1_thread.start()
        threads.append(dpir1_thread)
        print("DPIR1 sumilator started")
    else:
        print("Starting DPIR1 loop")
        dpir1 = PIR(settings["pin"], dpir1_callback)
        dpir1_thread = threading.Thread(target = run_pir_loop, args=(dpir1, stop_event))
        dpir1_thread.start()
        threads.append(dpir1_thread)
        print("DPIR1 loop started")