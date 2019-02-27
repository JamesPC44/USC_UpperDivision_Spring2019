import random
import sys
import math
import re

k = int(sys.argv[1])

def randstr(length):
    s = ""
    for i in range(length):
        s += random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    return s

print(k)
for i in range(k):
    print(randstr(random.randint(1, 5)) + " " + randstr(random.randint(1, 5)))

