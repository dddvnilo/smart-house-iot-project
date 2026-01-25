try:
    import RPi.GPIO as GPIO
except:
    pass
import time


class UDS(object):
    def __init__(self,trig_pin, echo_pin, scan_delay,callback):
        self.callback = callback
        self.trig_pin = trig_pin
        self.echo_pin = echo_pin
        self.scan_delay = scan_delay

        GPIO.setup(self.trig_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)

    def get_distance(self):
        GPIO.output(self.trig_pin, False)
        time.sleep(0.2)
        GPIO.output(self.trig_pin, True)
        time.sleep(0.00001)
        GPIO.output(self.trig_pin, False)
        pulse_start_time = time.time()
        pulse_end_time = time.time()

        max_iter = 100

        iter = 0
        while GPIO.input(self.echo_pin) == 0:
            if iter > max_iter:
                return None
            pulse_start_time = time.time()
            iter += 1

        iter = 0
        while GPIO.input(self.echo_pin) == 1:
            if iter > max_iter:
                return None
            pulse_end_time = time.time()
            iter += 1

        pulse_duration = pulse_end_time - pulse_start_time
        distance = (pulse_duration * 34300)/2

        self.callback(distance)

def run_uds_loop(uds, stop_event):
    while True:
        if stop_event.is_set():
            break
        uds.get_distance()
        time.sleep(uds.scan_delay)
