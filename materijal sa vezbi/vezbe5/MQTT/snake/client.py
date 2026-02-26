from snake import Field, Snake
import curses
import time
import paho.mqtt.client as mqtt
import threading

def on_connect(client, userdata, flags, rc):
    client.subscribe("snake")

def main(screen):
    screen.timeout(0)

    # Init snake & field
    field = Field(10)
    snake = Snake("Joe")
    snake.set_field(field)

    client = mqtt.Client()
    client.on_connect = on_connect
    def on_message(client, userdata, msg):
        snake.set_direction(msg.payload.decode('utf-8'))
    client.on_message = on_message

    client.connect("localhost", 1883, 60)
    client.loop_start()
    
    while(True):
        # Move snake
        snake.move()
        # Render field
        field.render(screen)
        screen.refresh()
        
        time.sleep(.4)

if __name__ == '__main__':
    
    curses.wrapper(main)
