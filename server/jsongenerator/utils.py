import random
import string

from math import ceil, floor

from elizabeth import Internet, Personal, Datetime, Text

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

def generate_format_string(format):
    if format == "ipv4":
        internet = Internet()
        return internet.ip_v4()
    elif format == "ipv6":
        internet = Internet()
        return internet.ip_v6()
    elif format == "uri":
        internet = Internet()
        return internet.home_page()
    elif format == "uri" or format == "hostname":
        internet = Internet()
        return internet.home_page()
    elif format == "email":
        personal = Personal()
        return personal.email()
    elif format == "date":
        datetime = Datetime()
        return datetime.date()
    elif format == "time":
        datetime = Datetime()
        return datetime.time()
    elif format == "age":
        personal = Personal()
        return personal.age()
    elif format == "full-name":
        personal = Personal()
        return personal.full_name()
    elif format == "username":
        personal = Personal()
        return personal.username()
    elif format == "name":
        personal = Personal()
        return personal.name()
    elif format == "surname":
        personal = Personal()
        return personal.surname()
    elif format == "password":
        personal = Personal()
        return personal.password()
    elif format == "title":
        text = Text()
        return text.quote()

