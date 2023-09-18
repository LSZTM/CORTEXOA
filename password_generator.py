import string
import random

def final_password():
    set = string.ascii_letters + string.digits + string.punctuation
    try:
        length = int(input("enter  desired length of password:"))
    except TypeError:
        print("TypeError: enter a number")
    password = ''.join([random.SystemRandom().choice(set) for _ in range(length)])
    return password

print(final_password())