lut = {
    19: "A",
    18: "B",
    8: "C",
    15: "D",
    20: "E",
    0: "F",
    6: "G",
    22: "H",
    1: "I",
    21: "J",
    13: "K",
    11: "L",
    12: "M",
    4: "N",
    24: "O",
    9: "P",
    10: "Q",
    16: "R",
    17: "S",
    3: "T",
    14: "U",
    23: "V",
    2: "W",
    25: "X",
    5: "Y",
    7: "Z",
}

import sys
import math
import re

n = int(sys.argv[1])
s = ""

s = lut[int((n % math.pow(26, 5)) / (math.pow(26, 4)))] + s
s = lut[int((n % math.pow(26, 4)) / (math.pow(26, 3)))] + s
s = lut[int((n % math.pow(26, 3)) / (math.pow(26, 2)))] + s
s = lut[int((n % math.pow(26, 2)) / (math.pow(26, 1)))] + s
s = lut[int((n % math.pow(26, 1)) / (math.pow(26, 0)))] + s

print(re.sub(r'F+$', '', s))
