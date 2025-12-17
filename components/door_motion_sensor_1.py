def dpir1_callback(motion):
    print("\n"+"="*20)
    if motion:
        print("DPIR1: Motion detected!")
    else:
        print("DPIR1: Motion stopped.")

def run_dpir1(settings, threads, stop_event):
    if settings['simulated']:
        print("kod simulacije za dpir1")
    else:
        print("kod za dpir1")