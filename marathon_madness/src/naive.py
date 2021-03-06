import sys
import math

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

def frag2int(s):
    n = 0
    i = 0
    for c in s:
        n += math.pow(26, i) * lut[c]
        i += 1

    return int(n)

# drop k
sys.stdin.readline()


points = []
for line in sys.stdin:
    points.append([frag2int(f) for f in line.split()] + line.split())

# https://medium.com/@andriylazorenko/closest-pair-of-points-in-python-79e2409fc0b2

def dist(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

def sort_internal(p1, p2):
    if (p1[0] > p2[0]):
        p1, p2 = p2, p1
    elif p1[0] == p2[0]:
        if (p1[1] > p2[1]):
            p1, p2 = p2, p1

    return p1, p2

best = 999999999999999
bestpts = []
for p1 in points:
    for p2 in points:
        if p1 == p2:
            continue
        d = dist(p1, p2)
        #  print(p1, p2, d)
        pair = [p1, p2]
        if d == best:
            if pair not in bestpts:
                if [p2, p1] not in bestpts:
                    bestpts.append(pair)
        elif d < best:
            best = d
            bestpts = [pair]

normalized_pairs = []
for p, q in bestpts:
    if (q[2], q[3]) < (p[2], p[3]):
        p, q = q, p
    normalized_pairs.append((p, q))

normalized_pairs.sort(key = lambda x: (x[0][2], x[0][3], x[1][2], x[1][3]))
for pair in normalized_pairs:
    print(" ".join([pair[0][2], pair[0][3], pair[1][2], pair[1][3]]))

#  for pair in sorted(bestpts, reverse=False):
#      #  sys.stderr.write(str(pair) + " " + str(dist(*pair)))
#      #  sys.stderr.write("\n")
#      print("{} {} {} {}".format(pair[0][2], pair[0][3], pair[1][2], pair[1][3]))
