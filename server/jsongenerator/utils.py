import random
import string


def generate_string(length):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def generate_number(min=0,max=1000):
    return random.randint(min, max)