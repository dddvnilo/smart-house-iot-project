import threading
from settings import load_settings
from components import run_ds1, run_dus1, run_dpir1, run_dht3, run_4sd, run_gsg, run_btn
import paho.mqtt.client as mqtt
import time
import json

try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
except:
    pass

display = None

def display_set_values(client, userdata, message):
    # postavi vrednosti
    data = json.loads(message.payload.decode())
    if not display:
        print("nema display-a")
        return
    
    value = data.get("display")
    if value is not None:
        display.set_value(str(value).rjust(4)[:4])  # uvek 4 cifre (ne mora ovde jer vec to radi klasa al za svaki slucaj)

    blinking = data.get("is_blinking")
    if blinking is not None:
        display.set_blinking(bool(blinking))

def on_connect(client, userdata, flags, rc):
    client.subscribe([ 
        ("home/kitchen/display-set-values", 0),
        ])

def on_disconnect(client, userdata, rc):
    print("Disconnected with result code", rc)

mqtt_client = mqtt.Client()

mqtt_client.on_connect = on_connect
mqtt_client.message_callback_add("home/kitchen/display-set-values", display_set_values)

# MQTT Configuration
mqtt_client.connect("127.0.0.1", 1883, 60)
mqtt_client.loop_start()

mqtt_client.on_disconnect = on_disconnect

if __name__ == "__main__":
    print('Starting app')
    settings = load_settings()
    threads = []
    stop_event = threading.Event()
    try:
        
        # ucitavanje podesavanja i pokretanje komponenti

        ds1_settings = settings['DS2']
        run_ds1(ds1_settings, threads, stop_event)

        dus1_settings = settings['DUS2']
        run_dus1(dus1_settings, threads, stop_event)

        dpir1_settings = settings['DPIR2']
        run_dpir1(dpir1_settings, threads, stop_event)
        
        gsg_settings = settings['GSG']
        run_gsg(gsg_settings, threads, stop_event)

        dht3_settings = settings['DHT3']
        run_dht3(dht3_settings, threads, stop_event)


        display_settings = settings['4SD']
        display = run_4sd(display_settings, threads, stop_event)

        btn_settings = settings['BTN']
        btn = run_btn(btn_settings, threads, stop_event)

        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print('Stopping app')
        for t in threads:
            stop_event.set()