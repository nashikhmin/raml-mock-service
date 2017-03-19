import random
import string


def generate_string_between(min_length, max_length):
    return generate_string(generate_int(min_length, max_length))


def generate_string(length):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))


def generate_int(min=0, max=1000):
    return random.randint(min, max)

def generate_float(min=0, max=1000):
    return random.uniform(min, max)
