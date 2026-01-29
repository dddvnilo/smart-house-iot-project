# bucket_settings.py
from enum import Enum

class BucketNames(Enum):
    DOOR_MEMBRANE_SWITCH = "door_membrane_switch"
    DOOR_MOTION_SENSOR = "door_motion_sensor"
    DOOR_ULTRASONIC_SENSOR = "door_ultrasonic_sensor"
    DOOR_SENSOR = "door_sensor"
    ACTUATORS = "actuators"