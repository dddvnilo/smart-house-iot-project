def dms_callback(key):
    print("\n"+"="*20)
    print(f"DMS: Key pressed: {key}")

def run_dms(settings, threads, stop_event):
    if settings['simulated']:
        print("kod simulacije za dms")
    else:
        print("kod za dms")