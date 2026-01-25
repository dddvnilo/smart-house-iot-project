try:
    import RPi.GPIO as GPIO
    from utils import PULL_MAP
except:
    pass
import time


class MembraneKeypad(object):
    def __init__(self, pin_rows, pin_cols, scan_delay, callback):
        self.pin_rows = pin_rows
        self.pin_cols = pin_cols
        self.scan_delay = scan_delay
        self.callback = callback
        for rpin in self.pin_rows:
            GPIO.setup(rpin, GPIO.OUT)

        for cpin in self.pin_cols:
            GPIO.setup(cpin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        
    def read_line(self, line, characters):
        GPIO.output(line, GPIO.HIGH)
        if(GPIO.input(self.pin_cols[0]) == 1):
            self.callback(characters[0])
        if(GPIO.input(self.pin_cols[0]) == 1):
            self.callback(characters[1])
        if(GPIO.input(self.pin_cols[0]) == 1):
            self.callback(characters[2])
        if(GPIO.input(self.pin_cols[0]) == 1):
            self.callback(characters[3])
        GPIO.output(line, GPIO.LOW)

    def read_all_lines(self):
        self.readLine(self.pin_rows[0], ["1","2","3","A"])
        self.readLine(self.pin_rows[1], ["4","5","6","B"])
        self.readLine(self.pin_rows[2], ["7","8","9","C"])
        self.readLine(self.pin_rows[3], ["*","0","#","D"])

def run_membrane_keypad_loop(mk, stop_event):
    while True:
        if stop_event.is_set():
            break
        mk.read_all_lines()
        time.sleep(mk.scan_delay)