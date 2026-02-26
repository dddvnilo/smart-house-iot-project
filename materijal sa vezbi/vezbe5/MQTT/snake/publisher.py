import paho.mqtt.client as mqtt


def main():

    client = mqtt.Client()
    client.connect("localhost", 1883, 60)

    while True:
        t = input()
        if t == 'w':
            client.publish('snake', 'UP')
        elif t == 'a':
            client.publish('snake', 'LEFT')
        elif t == 's':
            client.publish('snake', 'DOWN')
        elif t == 'd':
            client.publish('snake', 'RIGHT')
        else:
            print('invalid input')

if __name__ == '__main__':
    main()