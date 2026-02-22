try:
    import RPi.GPIO as GPIO
    from utils import PULL_MAP
except:
    pass
import time


class Membrane_keypad(object):
    def __init__(self,settings,callback, publish_event):
        self.pin_rows = settings["pin_rows"]
        self.pin_cols = settings["pin_cols"]
        self.scan_delay = settings["scan_delay"]
        self.callback = callback

        self.settings = settings
        self.publish_event = publish_event

        for rpin in self.pin_rows:
            GPIO.setup(rpin, GPIO.OUT)

        for cpin in self.pin_cols:
            GPIO.setup(cpin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        
    def keypad_pressed(self, keypad):
        self.callback(keypad, self.settings, self.publish_event)

    def read_line(self, line, characters):
        GPIO.output(line, GPIO.HIGH)
        if(GPIO.input(self.pin_cols[0]) == 1):
            self.keypad_pressed(characters[0])
        if(GPIO.input(self.pin_cols[1]) == 1):
            self.keypad_pressed(characters[1])
        if(GPIO.input(self.pin_cols[2]) == 1):
            self.keypad_pressed(characters[2])
        if(GPIO.input(self.pin_cols[3]) == 1):
            self.keypad_pressed(characters[3])
        GPIO.output(line, GPIO.LOW)

    def read_all_lines(self):
        self.read_line(self.pin_rows[0], ["1","2","3","A"])
        self.read_line(self.pin_rows[1], ["4","5","6","B"])
        self.read_line(self.pin_rows[2], ["7","8","9","C"])
        self.read_line(self.pin_rows[3], ["*","0","#","D"])



def run_membrane_keypad_loop(mk, stop_event):
    while True:
        if stop_event.is_set():
            break
        mk.read_all_lines()
        time.sleep(mk.scan_delay)