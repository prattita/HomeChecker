import requests
import datetime
from random import random, randint
from time import sleep


def main_loop(port):
    temp_in_F = 65
    name = 'fake_temp_sensor' + str(randint(0, 5))
    while True:
        temp_in_F += .05 * (random() - .5)  # add some jitter
        if random() < 0.3:  # sometimes, move temp more
            temp_in_F += -random() if random() < 0.5 else random()
            temp_in_F = min(temp_in_F, 95)
            temp_in_F = max(temp_in_F, -10)
        ping(name, temp_in_F)
        sleep(1)


def ping(name, value):
    try:
        post = {
            'name': name,
            'timestamp': datetime.datetime.now().isoformat(),
            'temp_level': value,
        }
        r = requests.post('http://localhost:5000/api/temp', json=post)
        print("sent message: {}".format(post))
    except requests.exceptions.ConnectionError as e:
        print("couldn't connect (ignoring)")


if __name__ == '__main__':
    main_loop('COM5')
