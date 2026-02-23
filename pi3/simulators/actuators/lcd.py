import time
import random

class LCD_simulator(object):
    def __init__(self, settings, publish_event, callback):
        self.callback = callback
        self.settings = settings
        self.publish_event = publish_event
        self.refresh_time = settings["refresh_time"]
        self.sensors_data = []  # lista tuple [(line1, line2), ...]

        # hardkodovani pinovi i I2C adresa
        self.i2c_address = 0x27
        self.pin_rs = 0
        self.pin_e = 2
        self.pins_db = [4,5,6,7]
        self.backlight_pin = 3  # MCP pin za backlight

    def set_data(self, sensors_data):
        self.sensors_data = sensors_data

    def displayed(self,lcd_print):
        self.callback(lcd_print, self.settings, self.publish_event)

def generate_lcd_values():
    while True:
        # Simulacija temperature i vlaznosti
        temp = random.uniform(20, 30)
        hum = random.uniform(30, 70)
        line1 = f"Temp: {temp:.1f} C"
        line2 = f"Hum : {hum:.1f} %"
        yield (line1, line2)

def run_lcd_simulator(lcd_display, stop_event):
    gen = generate_lcd_values()
    while not stop_event.is_set():
        line1, line2 = next(gen)
        lcd_print = line1 + " " + line2
        lcd_display.displayed(lcd_print)
        time.sleep(lcd_display.refresh_time)