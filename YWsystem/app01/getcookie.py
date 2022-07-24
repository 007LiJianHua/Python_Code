import string
import random

all_data = string.digits + string.ascii_letters

def randomString():
    data = ""
    for i in range(1,31):
        data = data + random.choice(all_data)
    return data

if __name__ == '__main__':
    print(randomString())
















