import random
import string

from math import ceil, floor


def generate_string_between(min_length, max_length):
    return generate_string(generate_int(min_length, max_length))


def generate_string(length):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))


def generate_int(min=0, max=1000):
    return random.randint(ceil(min), floor(max))


def generate_bool():
    return bool(random.getrandbits(1))

def generate_float(min=0, max=1000):
    return random.uniform(min, max)
