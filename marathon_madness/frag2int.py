lut = {
    "A": 19,
    "B": 18,
    "C": 8,
    "D": 15,
    "E": 20,
    "F": 0,
    "G": 6,
    "H": 22,
    "I": 1,
    "J": 21,
    "K": 13,
    "L": 11,
    "M": 12,
    "N": 4,
    "O": 24,
    "P": 9,
    "Q": 10,
    "R": 16,
    "S": 17,
    "T": 3,
    "U": 14,
    "V": 23,
    "W": 2,
    "X": 25,
    "Y": 5,
    "Z": 7,
}

import sys
import math

n = 0

i = 0
for c in sys.argv[1]:
    n += math.pow(26, i) * lut[c]
    i += 1

print(int(n))
