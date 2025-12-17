def ds1_callback():
    print("\n"+"="*20)
    print("DS1: Door sensor activated.")

def run_ds1(settings, threads, stop_event):
    if settings['simulated']:
        print("kod simulacije za ds1")
    else:
        print("kod za ds1")