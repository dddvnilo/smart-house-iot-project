import threading
from settings import load_settings
from components import run_dpir3, run_brgb, run_ir, run_dht1, run_dht2, run_lcd
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

        # dpir3_settings = settings['DPIR3']
        # run_dpir3(dpir3_settings, threads, stop_event)

        # brgb_settings = settings['BRGB']
        # run_brgb(brgb_settings, threads, stop_event)

        # ir_settings = settings['IR']
        # run_ir(ir_settings, threads, stop_event)

        dht1_settings = settings['DHT1']
        run_dht1(dht1_settings, threads, stop_event)

        dht2_settings = settings['DHT2']
        run_dht2(dht2_settings, threads, stop_event)

        lcd_settings = settings['LCD']
        run_lcd(lcd_settings, threads, stop_event)

        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print('Stopping app')
        for t in threads:
            stop_event.set()