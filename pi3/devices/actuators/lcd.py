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

    def displayed(self,lcd_print):
        self.callback(lcd_print, self.settings, self.publish_event)

    def display(self):
        if self.sensors_data:
            line1, line2 = self.sensors_data[idx % len(self.sensors_data)] # line1 - temperatura | line2 - humidity
            self.lcd.clear()
            self.lcd.setCursor(0,0)
            self.lcd.message(line1[:16])
            self.lcd.setCursor(0,1)
            self.lcd.message(line2[:16])
            idx += 1
            lcd_print = line1 + " " + line2
            self.displayed(lcd_print)

def run_lcd_loop(lcd_display, stop_event):
    idx = 0
    while stop_event.is_set():
        lcd_display.display()
        time.sleep(lcd_display.refresh_time)