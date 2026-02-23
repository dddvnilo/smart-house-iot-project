from flask import Flask, jsonify, request, Response
from influxdb_client import InfluxDBClient, Point, BucketRetentionRules, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import paho.mqtt.client as mqtt
import json
from bucket_settings import BucketNames
from pi_messenger import pi1_turn_alarm_on, pi1_turn_light_on, pi1_turn_alarm_off, pi3_lcd_set_values
import cv2
import math
import threading

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

a = 0
def check_alarm():
    global a
    a += 1
    if a == 1:
        pi1_turn_alarm_on()
    elif a == 3:
        pi1_turn_alarm_off()

people = 0

def check_people(name):
    global people
    direction = get_door_direction(name=name)
    people += direction
    if(people<0):
        people = 0
    print(people)

def on_dpir_message(client, userdata, message):
    data = json.loads(message.payload.decode('utf-8'))
    save_to_db(data, bucket=BucketNames.DOOR_MOTION_SENSOR.value)

    parts = message.topic.split("/")
    location = parts[1]  # front-door ili garage-door

    if location == "front-door":
        if data["value"]==True:
            print("Motion sa prednjih vrata")
            pi1_turn_light_on()
        else:
            check_people("Door ultrasonic sensor 1")
    elif location == "kitchen":
        if data["value"]==True:
            print("Motion iz kuhinje")
        else:
            check_people("Door ultrasonic sensor 2")

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

def on_rgb_message(client, userdata, message):
    data = json.loads(message.payload.decode('utf-8'))
    save_to_db(data, bucket=BucketNames.RGB_LED.value)

def on_ir_message(client, userdata, message):
    data = json.loads(message.payload.decode('utf-8'))
    save_to_db(data, bucket=BucketNames.IR.value)

def on_dht_message(client, userdata, message):
    data = json.loads(message.payload.decode('utf-8'))
    save_to_db(data, bucket=BucketNames.BEDROOM_DHT.value)

def on_4sd_message(client, userdata, message):
    data = json.loads(message.payload.decode('utf-8'))
    save_to_db(data, bucket=BucketNames.FOUR_DIGIT_DISPLAY.value)

    
# mzd treba napraviti ovako ness na globalnom fazonu
# definitivno ne boolean promenljiva al neki queue neka lista neki set
ALARM_ON = False
def on_gsg_message(client, userdata, message):
    global ALARM_ON

    ALARM_G_THRESHOLD = 1.5
    ALARM_DPS_THRESHOLD = 200.0

    # prag za iskljucenje da bude malo manji da nebi buzzer "trepereo", "stucao", "ludovao"
    ALARM_G_RESET = 1.2
    ALARM_DPS_RESET = 150.0

    data = json.loads(message.payload.decode('utf-8'))
    save_to_db(data, bucket=BucketNames.GYROSCOPE.value)

    if data.get("measurement") != "Gyroscope":
        return

    value_str = data.get("value")
    if not value_str:
        return

    try:
        x, y, z = map(float, value_str.split(","))
        magnitude = math.sqrt(x*x + y*y + z*z)
    except Exception:
        return

    if magnitude > ALARM_DPS_THRESHOLD and not ALARM_ON:
        pi1_turn_alarm_on()
        print("ALARM ON  | gyro magnitude:", magnitude)
        ALARM_ON = True

    elif magnitude < ALARM_DPS_RESET and ALARM_ON:
        pi1_turn_alarm_off()
        print("ALARM OFF | gyro magnitude:", magnitude)
        ALARM_ON = False

def on_lcd_message(client, userdata, message):
    data = json.loads(message.payload.decode('utf-8'))
    save_to_db(data, bucket=BucketNames.LCD.value)

# MQTT Configuration
mqtt_client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    client.subscribe([
        ("home/front-door/door_membrane_switch", 0), 
        ("home/front-door/door_motion_sensor", 0), 
        ("home/front-door/door_ultrasonic_sensor", 0), 
        ("home/front-door/door_sensor", 0),
        ("home/front-door/door_light", 0),
        ("home/front-door/door_buzzer", 0),
        ("home/bedroom/rgb_led", 0),
        ("home/bedroom/infrared_receiver", 0),
        ("home/bedroom/dht", 0),
        ("home/master-bedroom/dht", 0),
        ("home/kitchen/dht", 0),
        ("home/kitchen/display", 0),
        ("home/dining-room/gyroscope", 0),
        ("home/living-room/lcd", 0)
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
mqtt_client.message_callback_add("home/bedroom/rgb_led", on_rgb_message)
mqtt_client.message_callback_add("home/bedroom/infrared_receiver", on_ir_message)
mqtt_client.message_callback_add("home/+/dht", on_dht_message)
mqtt_client.message_callback_add("home/+/display", on_4sd_message)
mqtt_client.message_callback_add("home/+/gyroscope", on_gsg_message)
mqtt_client.message_callback_add("home/+/lcd", on_lcd_message)
# Ovaj plus je 'wildcard' za bilo koje ime, tako da ako stigne poruka na "home/front-door/door_sensor" ili "home/kitchen/door_sensor", oba vode na isti handler
# Za dalje, mozemo ili napraviti odvojene handlere za to sa kog topica je stiglo, ili u ovom handleru dodati tipa e ako je bas stiglo iz kuhinje uradi nesto drugacije

mqtt_client.on_disconnect = on_disconnect
mqtt_client.connect("127.0.0.1", 1883, 60)
mqtt_client.loop_start()


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

def get_door_direction(
    name,
    bucket: str = "door_ultrasonic_sensor",
    threshold_cm: float = 3.0
) -> str:
    """
    Checks last 4 seconds of ultrasonic distance data
    and determines movement direction.
    """

    flux_query = f"""
    data = from(bucket: "{bucket}")
      |> range(start: -4s)
      |> filter(fn: (r) => r._measurement == "Distance")
      |> filter(fn: (r) => r._field == "measurement")    
      |> filter(fn: (r) => r.name == "{name}")


    firstHalf = data
      |> range(start: -4s, stop: -2s)
      |> mean()

    secondHalf = data
      |> range(start: -2s)
      |> mean()

    join(
      tables: {{f: firstHalf, s: secondHalf}},
      on: ["_measurement", "_field"]
    )
    |> map(fn: (r) => ({{
        diff: r._value_s - r._value_f
    }}))
    """

    try:
        query_api = influxdb_client.query_api()
        tables = query_api.query(flux_query, org=org)

        for table in tables:
            for record in table.records:

                diff = record["diff"]

                if diff < 0:
                    return 1
                else:
                    return -1
    except Exception as e:
        return 0
    return 0


def get_last_dht_values():
    query = f'''
    from(bucket: "{BucketNames.BEDROOM_DHT.value}")
      |> range(start: -1h)
      |> filter(fn: (r) =>
          r._measurement == "Temperature" or
          r._measurement == "Humidity"
      )
      |> group(columns: ["name", "_measurement"])
      |> last()
    '''

    tables = influxdb_client.query_api().query(query, org=org)

    dht = {}

    for table in tables:
        for r in table.records:
            name = r["name"]
            meas = r["_measurement"]
            val = r["_value"]

            if name not in dht:
                dht[name] = {"temp": None, "hum": None}

            if meas == "Temperature":
                dht[name]["temp"] = val
            else:
                dht[name]["hum"] = val

    name_map = {
    "Bedroom DHT": "DHT1",
    "Master Bedroom DHT": "DHT2",
    "Kitchen DHT": "DHT3"
    }

    result = []

    for influx_name, label in name_map.items():
        if influx_name in dht:
            temp = dht[influx_name]["temp"]
            hum  = dht[influx_name]["hum"]

            if temp is not None and hum is not None:
                line1 = f"{label} T:{temp:.1f}C"
                line2 = f"{label} H:{hum:.1f}%"
                result.append((line1, line2))

    return result

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

def generate_mjpeg(camera_url=None, fallback_video="fallback.avi"):
    cap = None

    if camera_url:
        cap = cv2.VideoCapture(camera_url)

    # fallback ako nema kamere
    if not cap or not cap.isOpened():
        print("Camera not available -> using fallback video")
        cap = cv2.VideoCapture(fallback_video)

    while True:
        success, frame = cap.read()

        if not success:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue

        ret, jpeg = cv2.imencode('.jpg', frame)
        if not ret:
            continue

        yield (
            b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' +
            jpeg.tobytes() +
            b'\r\n'
        )

@app.route('/camera_stream')
def camera_stream():
    camera_url = "http://<raspberry_pi_ip>:8080/?action=stream"

    return Response(
        generate_mjpeg(camera_url=camera_url, fallback_video="resources/static.mjpeg.avi"),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )

# salje LCD-u najnovije zapisane vrednosti
def lcd_update():
    # dobavi poslednje upisane vrednosti u bazu
    values = get_last_dht_values()
    # spakuj u payload
    payload = json.dumps({
        "lines": values
    })
    # posalji lcd-u
    pi3_lcd_set_values(payload)
    threading.Timer(10, lcd_update).start()  # zakazuje sledeći update

if __name__ == '__main__':
    lcd_update()
    app.run(debug=False ,use_reloader=False)
