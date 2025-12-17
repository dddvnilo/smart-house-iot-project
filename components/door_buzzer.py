def db_callback(pitch, duration):
    print("\n"+"="*20)
    print(f"DB: Buzzer activated - pitch: {pitch}Hz, duration: {duration}s")

def run_db(settings, threads, stop_event):
    if settings['simulated']:
        print("kod simulacije za db")
    else:
        print("kod za db")