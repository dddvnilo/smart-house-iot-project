from simulators.sensors.uds import run_uds_simulator
import threading
import time

def dus1_callback(distance):
    t = time.localtime()
    print("\n"+"="*20)
    print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    print(f"DUS1: Distance measured: {distance:.2f} cm")

def run_dus1(settings, threads, stop_event):
    if settings['simulated']:
        print("Starting DUS1 simulator")
        dl_thread = threading.Thread(target = run_uds_simulator, args=(dus1_callback, stop_event, settings['scan_delay']))
        dl_thread.start()
        threads.append(dl_thread)
        print("DUS1 sumilator started")
    else:
        print("Starting DUS1 loop")
        print("DUS1 loop started")