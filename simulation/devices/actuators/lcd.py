try:
    from lcd_utils.PCF8574 import PCF8574_GPIO
    from lcd_utils.Adafruit_LCD1602 import Adafruit_CharLCD
except:
    pass

import time
import threading

class LCD(object):
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

        # inicijalizacija MCP i LCD
        try:
            self.mcp = PCF8574_GPIO(self.i2c_address)
        except Exception as e:
            print(f"I2C Address Error! {e}")
            raise

        self.lcd = Adafruit_CharLCD(pin_rs=self.pin_rs,
                                    pin_e=self.pin_e,
                                    pins_db=self.pins_db,
                                    GPIO=self.mcp)
        self.mcp.output(self.backlight_pin, 1)  # backlight ON
        self.lcd.begin(16,2)

    def set_data(self, sensors_data):
        self.sensors_data = sensors_data

def run_lcd_loop(display, stop_event):
    idx = 0
    while stop_event.is_set():
        if display.sensors_data:
            line1, line2 = display.sensors_data[idx % len(display.sensors_data)] # line1 - temperatura | line2 - humidity
            display.lcd.clear()
            display.lcd.setCursor(0,0)
            display.lcd.message(line1[:16])
            display.lcd.setCursor(0,1)
            display.lcd.message(line2[:16])
            idx += 1
            lcd_print = line1 + " " + line2
            display.callback(lcd_print, display.settings, display.publish_event)
        time.sleep(display.refresh_time)