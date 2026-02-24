import threading
from settings import load_settings
from components import run_dpir3, run_brgb, run_ir, run_dht1, run_dht2, run_lcd
import paho.mqtt.client as mqtt
import time
import json

try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
except:
    pass

lcd = None
rgb_led = None

def lcd_set_values(client, userdata, message):
    # postavi vrednosti
    data = json.loads(message.payload.decode())
    lines = data.get("lines", [])
    if not lcd:
        return
    lcd.set_data(lines)

def rgb_led_set_input(client, userdata, message):
    data = json.loads(message.payload.decode())
    ir_input = data.get("input")

    if not rgb_led:
        return
    
    rgb_led.led_input(ir_input)

def on_connect(client, userdata, flags, rc):
    client.subscribe([ 
        ("home/living-room/lcd-set-values", 0),
        ("home/bedroom/rgb_led-set-input", 0)
        ])

def on_disconnect(client, userdata, rc):
    print("Disconnected with result code", rc)

mqtt_client = mqtt.Client()

mqtt_client.on_connect = on_connect
mqtt_client.message_callback_add("home/living-room/lcd-set-values", lcd_set_values)
mqtt_client.message_callback_add("home/bedroom/rgb_led-set-input", rgb_led_set_input)

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

        '''
        dpir3_settings = settings['DPIR3']
        run_dpir3(dpir3_settings, threads, stop_event)

        dht1_settings = settings['DHT1']
        run_dht1(dht1_settings, threads, stop_event)

        dht2_settings = settings['DHT2']
        run_dht2(dht2_settings, threads, stop_event)

        lcd_settings = settings['LCD']
        lcd = run_lcd(lcd_settings, threads, stop_event)
        '''

        brgb_settings = settings['BRGB']
        rgb_led = run_brgb(brgb_settings, threads, stop_event)

        ir_settings = settings['IR']
        run_ir(ir_settings, threads, stop_event)

        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print('Stopping app')
        for t in threads:
            stop_event.set()