def dus1_callback(distance):
    print("\n"+"="*20)
    print(f"DUS1: Distance measured: {distance:.2f} cm")

def run_dus1(settings, threads, stop_event):
    if settings['simulated']:
        print("kod simulacije za dus1")
    else:
        print("kod za dus1")