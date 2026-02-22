try:
    from gyroscope_utils import MPU6050
except:
    pass

import time


class Gyroscope(object):
    def __init__(self, settings, callback, publish_event):
        self.settings = settings
        self.callback = callback
        self.publish_event = publish_event
        self.scan_delay = settings.get("scan_delay", 0.1)

        self.mpu = MPU6050.MPU6050()
        self.mpu.dmp_initialize()

    def send_gyro_data(self, data):
        self.callback(data, self.settings, self.publish_event)

    def read_sensor(self):
        try:
            accel = self.mpu.get_acceleration()
            gyro = self.mpu.get_rotation()

            # konverzija u fizicke jedinice
            accel_g = [a / 16384.0 for a in accel]
            gyro_dps = [g / 131.0 for g in gyro]

            data = {
                "accel_raw": accel,
                "gyro_raw": gyro,
                "accel_g": accel_g,
                "gyro_dps": gyro_dps
            }

            # pozovi callback
            self.send_gyro_data(data)

            return True

        except Exception as e:
            print("MPU read error:", e)
            return False
        
def run_gsg_loop(mpu_sensor, stop_event):
    while not stop_event.is_set():
        mpu_sensor.read_sensor()
        time.sleep(mpu_sensor.scan_delay)