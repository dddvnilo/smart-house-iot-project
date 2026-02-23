import threading
from settings import load_settings
from components import run_ds1, run_dl, run_dus1, run_db, run_dpir1, run_dms
import paho.mqtt.client as mqtt
import json
import time
from broker_settings import HOSTNAME, PORT

try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
except:
    pass

ds1 = None
dl = None
dus1 = None
db = None
dpir1 = None
dms = None
alarm_stop_event = None

def light_on_motion(client, userdata, message):
    print("SVETLOLOLO")
    dl.turn_led_on_for_ten_seconds()

def alarm_on(client, userdata, message):
    print("ALARMMMMMM")
    db.alarm_buzz(True)

def alarm_off(client, userdata, message):
    print("Nema alarma")
    db.alarm_buzz(False)

def on_connect(client, userdata, flags, rc):
    client.subscribe([ 
        ("home/front-door/light-on", 0),
        ("home/front-door/alarm-on", 0),
        ("home/front-door/alarm-off", 0),
        ])

def on_disconnect(client, userdata, rc):
    print("Disconnected with result code", rc)

mqtt_client = mqtt.Client()

mqtt_client.on_connect = on_connect
mqtt_client.message_callback_add("home/front-door/light-on", light_on_motion)
mqtt_client.message_callback_add("home/front-door/alarm-on", alarm_on)
mqtt_client.message_callback_add("home/front-door/alarm-off", alarm_off)


# MQTT Configuration
mqtt_client.connect(HOSTNAME, PORT, 60)
mqtt_client.loop_start()


# Ovaj plus je 'wildcard' za bilo koje ime, tako da ako stigne poruka na "home/front-door/door_sensor" ili "home/kitchen/door_sensor", oba vode na isti handler
# Za dalje, mozemo ili napraviti odvojene handlere za to sa kog topica je stiglo, ili u ovom handleru dodati tipa e ako je bas stiglo iz kuhinje uradi nesto drugacije

mqtt_client.on_disconnect = on_disconnect


if __name__ == "__main__":
    print('Starting app')
    settings = load_settings()
    threads = []
    stop_event = threading.Event()
    try:
        
        # ucitavanje podesavanja i pokretanje komponenti
        
        #ds1_settings = settings['DS1']
        #ds1 = run_ds1(ds1_settings, threads, stop_event)

        dl_settings = settings['DL']
        dl = run_dl(dl_settings, threads, stop_event)

        dus1_settings = settings['DUS1']
        dus1 = run_dus1(dus1_settings, threads, stop_event)

        db_settings = settings['DB']
        db = run_db(db_settings, threads, stop_event)

        dpir1_settings = settings['DPIR1']
        dpir1 = run_dpir1(dpir1_settings, threads, stop_event)

        #dms_settings = settings['DMS']
        #dms = run_dms(dms_settings, threads, stop_event)

        
        while True:
            time.sleep(0.1)

    except KeyboardInterrupt:
        print('Stopping app')
        for t in threads:
            stop_event.set()