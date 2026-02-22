import time
import random

def generate_lcd_values():
    while True:
        # Simulacija temperature i vlaznosti
        temp = random.uniform(20, 30)
        hum = random.uniform(30, 70)
        line1 = f"Temp: {temp:.1f} C"
        line2 = f"Hum : {hum:.1f} %"
        yield (line1, line2)

def run_lcd_simulator(callback, stop_event, settings, publish_event):
    gen = generate_lcd_values()
    while not stop_event.is_set():
        line1, line2 = next(gen)
        lcd_print = line1 + " " + line2
        callback(lcd_print, settings=settings, publish_event=publish_event)
        time.sleep(settings.get("refresh_time", 1.0))