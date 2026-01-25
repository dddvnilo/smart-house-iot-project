from simulators.sensors.membrane_keypad import run_membrane_keypad_simulator
import threading
import time
from devices.sensors.membrane_keypad import MembraneKeypad, run_membrane_keypad_loop

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
        print("Starting DMS loop")
        dms = MembraneKeypad(settings["pin_rows"], settings["pin_cols"], settings["scan_delay"], dms_callback)
        dms_thread = threading.Thread(target = run_membrane_keypad_loop, args=(dms, stop_event))
        dms_thread.start()
        threads.append(dms_thread)
        print("DMS loop started")