from simulators.sensors.membrane_keypad import run_membrane_keypad_simulator
import threading
import time

def dms_callback(key):
    t = time.localtime()
    print("\n"+"="*20)
    print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    print(f"DMS: Key pressed: {key}")

def run_dms(settings, threads, stop_event):
    if settings['simulated']:
        print("Starting DMS simulator")
        dms_thread = threading.Thread(target = run_membrane_keypad_simulator, args=(dms_callback, stop_event, settings['scan_delay']))
        dms_thread.start()
        threads.append(dms_thread)
        print("DMS sumilator started")
    else:
        print("kod za dms")