from simulators.actuators.buzzer import run_buzzer_simulator
import threading
import time
from devices.actuators.buzzer import Buzzer, run_buzz_loop

def db_callback():
    t = time.localtime()
    print("\n"+"="*20)
    print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    print("DB: Buzz buzz")

def run_db(settings, threads, stop_event):
    if settings['simulated']:
        print("Starting DB simulator")
        db_thread = threading.Thread(target = run_buzzer_simulator, args=(db_callback, stop_event))
        db_thread.start()
        threads.append(db_thread)
        print("DB sumilator started")
    else:
        print("Starting DB loop")
        db = Buzzer(settings["pin"], settings["pitch"], settings["duration"], db_callback)
        db_thread = threading.Thread(target = run_buzz_loop, args=(db, stop_event))
        db_thread.start()
        threads.append(db_thread)
        print("DB loop started")