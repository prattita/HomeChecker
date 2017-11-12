import serial
import requests
import json
import datetime


def main_loop(port):
    while True:
        # try:
        with serial.Serial(port, 9600, timeout=30) as ser:
            ser.flushInput()
            while True:
                ping(ser.readline().decode("ascii").rstrip('\r\n'))


def ping(raw):
    try:
        data = json.loads(raw)[0]
        post = {
            'name': data['sensor'],
            'timestamp': datetime.datetime.now().isoformat(),
            'light_level': data['light_level']
        }
        r = requests.post('http://localhost:5000/api/light', json=post)
        print("sent message: {}".format(data))
    except json.JSONDecodeError as e:
        # maybe we started reading in the middle of a line
        print("couldn't decode data: {}".format(raw))
    except requests.exceptions.ConnectionError as e:
        print("couldn't connect (ignoring)")


if __name__ == '__main__':
    main_loop('COM5')
