import threading
import time
import json
import paho.mqtt.publish as publish
from broker_settings import PI1_HOSTNAME, PI2_HOSTNAME, PI3_HOSTNAME, PORT


def pi1_turn_light_on():
    publish.single("home/front-door/light-on", hostname=PI1_HOSTNAME, port=PORT)
    print("Ukljuci svetlo na pi1")

def pi1_turn_alarm_on():
    publish.single("home/front-door/alarm-on", hostname=PI1_HOSTNAME, port=PORT)
    # upisi u bazu da je alarm ukljucen...
    print("Ukljuci alarm na pi1")

def pi1_turn_alarm_off():
    publish.single("home/front-door/alarm-off", hostname=PI1_HOSTNAME, port=PORT)
    # upisi u bazu da je alarm iskljucen...
    print("Iskljuci alarm na pi1")

def pi3_lcd_set_values(payload):
    publish.single("home/living-room/lcd-set-values", payload=payload, hostname=PI3_HOSTNAME, port=PORT)
    print("Postavi nove vrednosti na LCD")

def pi2_display_set_values(payload):
    publish.single("home/kitchen/display-set-values", payload=payload, hostname=PI2_HOSTNAME, port=PORT)
