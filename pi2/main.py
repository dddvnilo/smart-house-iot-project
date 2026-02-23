import threading
from settings import load_settings
from components import run_ds1, run_dus1, run_dpir1, run_dht1, run_4sd, run_gsg
import time

try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
except:
    pass

if __name__ == "__main__":
    print('Starting app')
    settings = load_settings()
    threads = []
    stop_event = threading.Event()
    try:
        
        # ucitavanje podesavanja i pokretanje komponenti
        '''
        ds1_settings = settings['DS1']
        run_ds1(ds1_settings, threads, stop_event)

        dus1_settings = settings['DUS1']
        run_dus1(dus1_settings, threads, stop_event)

        dpir1_settings = settings['DPIR1']
        run_dpir1(dpir1_settings, threads, stop_event)

        dht1_settings = settings['DHT1']
        run_dht1(dht1_settings, threads, stop_event)

        display_settings = settings['4SD']
        run_4sd(display_settings, threads, stop_event)

        display_settings = settings['4SD']
        run_4sd(display_settings, threads, stop_event)
        '''
        gsg_settings = settings['GSG']
        run_gsg(gsg_settings, threads, stop_event)

        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print('Stopping app')
        for t in threads:
            stop_event.set()