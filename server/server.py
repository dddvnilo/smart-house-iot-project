from flask import Flask, jsonify, request
from influxdb_client import InfluxDBClient, Point, BucketRetentionRules, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import paho.mqtt.client as mqtt
import json
from bucket_settings import BucketNames

app = Flask(__name__)


# InfluxDB Configuration
token = "superToken"
org = "FTN"
url = "http://localhost:8086"
failsafe_bucket = "iot_smart_house"
influxdb_client = InfluxDBClient(url=url, token=token, org=org)

# Creating buckets
buckets_api = influxdb_client.buckets_api()

for comp in BucketNames:
    bucket_name = comp.value
    existing_buckets = [b.name for b in buckets_api.find_buckets().buckets]
    if bucket_name not in existing_buckets:
        buckets_api.create_bucket(bucket_name=bucket_name, org=org, retention_rules=BucketRetentionRules(type="expire", every_seconds=0))
        print(f"Bucket '{bucket_name}' has been created")
    else:
        print(f"Bucket '{bucket_name}' already exists")

# Defining MQTT message handlers

def on_dms_message(client, userdata, message):
    # 
    data = json.loads(message.payload.decode('utf-8'))
    save_to_db(data, bucket=BucketNames.DOOR_MEMBRANE_SWITCH.value)

def on_dpir_message(client, userdata, message):
    data = json.loads(message.payload.decode('utf-8'))
    save_to_db(data, bucket=BucketNames.DOOR_MOTION_SENSOR.value)

def on_dus_message(client, userdata, message):
    data = json.loads(message.payload.decode('utf-8'))

    save_to_db(data, bucket=BucketNames.DOOR_ULTRASONIC_SENSOR.value)

def on_ds_message(client, userdata, message):
    data = json.loads(message.payload.decode('utf-8'))
    save_to_db(data, bucket=BucketNames.DOOR_SENSOR.value)

def on_dl_message(client, userdata, message):
    data = json.loads(message.payload.decode('utf-8'))
    save_to_db(data, bucket=BucketNames.DOOR_LIGHT.value)

def on_db_message(client, userdata, message):
    data = json.loads(message.payload.decode('utf-8'))
    save_to_db(data, bucket=BucketNames.DOOR_BUZZER.value)

# MQTT Configuration
mqtt_client = mqtt.Client()
mqtt_client.connect("127.0.0.1", 1883, 60)
mqtt_client.loop_start()

def on_connect(client, userdata, flags, rc):
    client.subscribe([
        ("home/front-door/door_membrane_switch", 0), 
        ("home/front-door/door_motion_sensor", 0), 
        ("home/front-door/door_ultrasonic_sensor", 0), 
        ("home/front-door/door_sensor", 0),
        ("home/front-door/door_light", 0),
        ("home/front-door/door_buzzer", 0)
        # posle cemo imati tipa ("home/kitchen/door_sensor", 0)
        ])

def on_disconnect(client, userdata, rc):
    print("Disconnected with result code", rc)

mqtt_client.on_connect = on_connect
mqtt_client.on_message = lambda client, userdata, msg: save_to_db(json.loads(msg.payload.decode('utf-8')))
mqtt_client.message_callback_add("home/+/door_membrane_switch", on_dms_message)
mqtt_client.message_callback_add("home/+/door_motion_sensor", on_dpir_message)
mqtt_client.message_callback_add("home/+/door_ultrasonic_sensor", on_dus_message)
mqtt_client.message_callback_add("home/+/door_sensor", on_ds_message)
mqtt_client.message_callback_add("home/+/door_light", on_dl_message)
mqtt_client.message_callback_add("home/+/door_buzzer", on_db_message)
# Ovaj plus je 'wildcard' za bilo koje ime, tako da ako stigne poruka na "home/front-door/door_sensor" ili "home/kitchen/door_sensor", oba vode na isti handler
# Za dalje, mozemo ili napraviti odvojene handlere za to sa kog topica je stiglo, ili u ovom handleru dodati tipa e ako je bas stiglo iz kuhinje uradi nesto drugacije

mqtt_client.on_disconnect = on_disconnect
    

def save_to_db(data, bucket = failsafe_bucket):
    write_api = influxdb_client.write_api(write_options=SYNCHRONOUS)
    point = (
        Point(data["measurement"])
        .tag("simulated", data["simulated"])
        .tag("runs_on", data["runs_on"])
        .tag("name", data["name"])
        .field("measurement", data["value"])
        .time(int(data["timestamp"] * 1000), WritePrecision.MS)
    )
    write_api.write(bucket=bucket, org=org, record=point)


# Route to store dummy data
@app.route('/store_data', methods=['POST'])
def store_data():
    try:
        data = request.get_json()
        store_data(data)
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


def handle_influx_query(query):
    try:
        query_api = influxdb_client.query_api()
        tables = query_api.query(query, org=org)

        container = []
        for table in tables:
            for record in table.records:
                container.append(record.values)

        return jsonify({"status": "success", "data": container})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


@app.route('/simple_query', methods=['GET'])
def retrieve_simple_data():
    query = f"""from(bucket: "door_ultrasonic_sensor")
  |> range(start: -5h)                     // proverava poslednjih 5 sati
  |> filter(fn: (r) => r._measurement == "Distance")
  |> keep(columns: ["_time", "_value", "simulated", "runs_on", "name"])
  |> sort(columns: ["_time"])"""
    return handle_influx_query(query)

# Ovako sam proverio dal se zapisuje za door senror preko grafane
""" 
from(bucket: "door_sensor")
  |> range(start: -5h)                     // proverava poslednjih 5 sati
  |> filter(fn: (r) => r._measurement == "IsUnlocked") // Ovde ne zaboravi da promenis koja je merna jedinica
  |> keep(columns: ["_time", "_value", "simulated", "runs_on", "name"])
  |> sort(columns: ["_time"])
"""


@app.route('/aggregate_query', methods=['GET'])
def retrieve_aggregate_data():
    query = f"""from(bucket: "{failsafe_bucket}")
    |> range(start: -10m)
    |> filter(fn: (r) => r._measurement == "Humidity")
    |> mean()"""
    return handle_influx_query(query)


if __name__ == '__main__':
    app.run(debug=True)
