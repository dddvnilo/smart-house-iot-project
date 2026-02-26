import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import math
import time
import json

def generate_temperature():
    amplitude = 5
    frequency = 0.1
    offset = 20
    timestamp = int(time.time())

    temperature = amplitude * math.sin(frequency * timestamp) + offset

    payload = {
        "measurement": "Temperature",
        "tag1": "tag1",
        "tag2": "tag2",
        "value": temperature
    }

    return json.dumps(payload)

def main():
    client = mqtt.Client()
    client.connect("localhost", 1883, 60)

    while True:
        temperature_batch = []
        for i in range(5):
            temperature_payload = generate_temperature()
            temperature_batch.append(('temperature', temperature_payload, 0, True))
            time.sleep(0.5)
        publish.multiple(temperature_batch)

if __name__ == '__main__':
    main()
