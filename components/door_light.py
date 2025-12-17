def dl_callback(state):
    print("\n"+"="*20)
    # state kao True/False
    if state:
        print("DL: Door Light turned ON")
    else:
        print("DL: Door Light turned OFF")

def run_dl(settings, threads, stop_event):
    if settings['simulated']:
        print("kod simulacije za dl")
    else:
        print("kod za dl")