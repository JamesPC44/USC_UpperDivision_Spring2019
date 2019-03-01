rule = list(reversed(list(map(int, bin(int(input()))[2:].zfill(8)))))
k = int(input())
inp = input()
first = list(map(int, list(str(inp))))
next = list(first)

for g in range(k):
    win1 = [first[-1], first[0], first[1]]
    idx1 = (win1[0] << 2) | (win1[1] << 1) | win1[2]
    next[0] = rule[idx1]

    for i in range(len(first) - 2):
        window = first[i:i+3]
        idx = (window[0] << 2) | (window[1] << 1) | window[2]
        next[i+1] = rule[idx]

    win2 = [first[-2], first[-1], first[0]]
    idx2 = (win2[0] << 2) | (win2[1] << 1) | win2[2]
    next[-1] = rule[idx2]
    print(''.join(map(str, next)))

    first = list(next)

print(''.join(map(str, next)))