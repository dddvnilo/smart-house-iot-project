try:
    import RPi.GPIO as GPIO
except:
    pass
import time

class DHT(object):
    DHT11_WAKEUP = 0.020  # 20ms
    TIMEOUT = 0.0001      # 100us

    def __init__(self, settings, callback, publish_event):
        self.pin = settings["pin"]
        self.settings = settings
        self.scan_delay = settings["scan_delay"]
        self.callback = callback
        self.publish_event = publish_event

        # GPIO pin setup
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, GPIO.HIGH)

    def read_sensor(self):
        bits = [0, 0, 0, 0, 0]
        mask = 0x80
        idx = 0

        # send wakeup signal
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, GPIO.LOW)
        time.sleep(self.DHT11_WAKEUP)
        GPIO.output(self.pin, GPIO.HIGH)
        GPIO.setup(self.pin, GPIO.IN)

        # wait for response
        loop_limit = 100
        start_time = time.time()
        while GPIO.input(self.pin) == GPIO.LOW:
            if (time.time() - start_time) > self.TIMEOUT:
                return False
        start_time = time.time()
        while GPIO.input(self.pin) == GPIO.HIGH:
            if (time.time() - start_time) > self.TIMEOUT:
                return False

        # read 40 bits
        for i in range(40):
            start_time = time.time()
            while GPIO.input(self.pin) == GPIO.LOW:
                if (time.time() - start_time) > self.TIMEOUT:
                    return False
            start_time = time.time()
            while GPIO.input(self.pin) == GPIO.HIGH:
                if (time.time() - start_time) > self.TIMEOUT:
                    return False
            if (time.time() - start_time) > 0.00005:  # >50us high = 1
                bits[idx] |= mask
            mask >>= 1
            if mask == 0:
                mask = 0x80
                idx += 1

        # parse bits
        humidity = bits[0]
        temperature = bits[2] + bits[3] * 0.1
        checksum = (bits[0] + bits[1] + bits[2] + bits[3]) & 0xFF
        if bits[4] != checksum:
            return False

        # call callback
        self.callback(humidity, temperature, self.settings, self.publish_event)
        return True

def run_dht_loop(dht, stop_event):
    while not stop_event.is_set():
        dht.read_sensor()
        time.sleep(dht.scan_delay)