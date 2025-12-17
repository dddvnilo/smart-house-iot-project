from simulators.actuators.buzzer import run_buzzer_simulator
import threading
import time

def db_callback(duration):
    t = time.localtime()
    print("\n"+"="*20)
    print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    print("DB: Buzz buzz")
    time.sleep(duration)  # trajanje buzz-a
    print("DB: Buzz ended\n")

def run_db(settings, threads, stop_event):
    if settings['simulated']:
        print("Starting DB1 simulator")
        db_thread = threading.Thread(target = run_buzzer_simulator, args=(db_callback, settings, stop_event))
        db_thread.start()
        threads.append(db_thread)
        print("DB1 sumilator started")
    else:
        print("Starting DB1 loop")
        print("DB1 loop started")