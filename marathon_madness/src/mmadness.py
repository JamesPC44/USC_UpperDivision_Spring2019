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
    points.append(tuple([frag2int(f) for f in line.split()] + line.split()))

# https://medium.com/@andriylazorenko/closest-pair-of-points-in-python-79e2409fc0b2

def dist(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

def closest_split_pair(p_x, p_y, delta, best_pairs):
    ln_x = len(p_x)  # store length - quicker
    mx_x = p_x[ln_x // 2][0]  # select midpoint on x-sorted array

    # Create a subarray of points not further than delta from
    # midpoint on x-sorted array

    s_y = [x for x in p_y if mx_x - delta <= x[0] <= mx_x + delta]

    best = delta  # assign best value to delta
    ln_y = len(s_y)  # store length of subarray for quickness
    for i in range(ln_y - 1):
        for j in range(i+1, min(i + 7, ln_y)):
            p, q = s_y[i], s_y[j]
            dst = dist(p, q)
            if dst == best:
                best_pairs.add((p, q))
            if dst < best:
                best_pair = {(p, q)}
                best = dst
    return best_pairs, best

def brute(ax):
    mi = dist(ax[0], ax[1])
    ps = {(ax[0], ax[1])}
    ln_ax = len(ax)
    if ln_ax == 2:
        return ps, mi
    for i in range(ln_ax-1):
        for j in range(i + 1, ln_ax):
            if i != 0 and j != 1:
                d = dist(ax[i], ax[j])
                if d == mi:
                    ps.add((ax[i], ax[j]))
                if d < mi:  # Update min_dist and points
                    mi = d
                    ps = {(ax[i], ax[j])}
    return ps, mi


def closest_pair(ax, ay):
    ln_ax = len(ax)  # It's quicker to assign variable
    if ln_ax <= 3:
        return brute(ax)  # A call to bruteforce comparison
    mid = ln_ax // 2  # Division without remainder, need int
    Qx = ax[:mid]  # Two-part split
    Rx = ax[mid:]

    # Determine midpoint on x-axis

    midpoint = ax[mid][0]  
    Qy = list()
    Ry = list()
    for x in ay:  # split ay into 2 arrays using midpoint
        if x[0] <= midpoint:
           Qy.append(x)
        else:
           Ry.append(x)

    # Call recursively both arrays after split

    pairs1, mi1 = closest_pair(Qx, Qy)
    pairs2, mi2 = closest_pair(Rx, Ry)

    # Determine smaller distance between points of 2 arrays

    if mi1 < mi2:
        d = mi1
        mns = pairs1
    elif mi2 < mi1:
        d = mi2
        mns = pairs2
    else:
        d = mi1
        mns = pairs1.union(pairs2)

    # Call function to account for points on the boundary

    pairs_final, d_final = closest_split_pair(ax, ay, d, mns)
    return pairs_final, d_final

    # Determine smallest distance for the array

    #if d <= mi3:
    #    return mn[0], mn[1], d
    #else:
    #    return p3, q3, mi3

ax = sorted(points, key=lambda x: x[0])  # Presorting x-wise
ay = sorted(points, key=lambda x: x[1])  # Presorting y-wise
pairs, mi = closest_pair(ax, ay)  # Recursive D&C function

normalized_pairs = []
for p, q in pairs:
    if " ".join([q[2], q[3]]) < " ".join([p[2], p[3]]):
        p, q = q, p
    normalized_pairs.append((p, q))

normalized_pairs.sort(key = lambda x: " ".join([x[0][2], x[0][3], x[1][2], x[1][3]]))
for pair in normalized_pairs:
    print(" ".join([pair[0][2], pair[0][3], pair[1][2], pair[1][3]]))

# p1, p2 = sorted([p1, p2], key=lambda x: x[0] + x[1])
# 
# sys.stderr.write(str(p1) + "\n"  + str(p2) + "\n" + str(mi) + "\n")
# sys.stderr.flush()
# print(p1[2], p1[3])
# print(p2[2], p2[3])
