import random
import sys
import math
import re

k = int(sys.argv[1])
j = int(sys.argv[2])
m = int(sys.argv[3])

seen = set()

def randstr(length):
    s = ""
    for i in range(length):
        s += random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    return s

print(k)
for i in range(k):
    while True:
        s = randstr(random.randint(j, m)) + " " + randstr(random.randint(j, m))
        if s not in seen:
            print(s)
            seen.update(s)
            break

