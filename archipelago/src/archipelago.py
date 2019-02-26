#!/usr/bin/python3

import sys

class DisjointSetForrest:
    def __init__(self, num_islands):
        self.num_islands = num_islands
        self.parents = [i for i in range(num_islands)]
        self.ranks = [0 for i in range(num_islands)]

    def find(self, elem):
        start_idx = elem
        idx = elem
        while self.parents[idx] != idx:
            idx = self.parents[idx]

        final_idx = idx
        idx = start_idx
        while self.parents[idx] != idx:
            parent_idx = self.parents[idx]
            self.parents[idx] = final_idx
            idx = parent_idx

        return final_idx

    def merge(self, elem_a, elem_b):
        head_a = self.find(elem_a)
        head_b = self.find(elem_b)

        if head_a == head_b:
            return

        if self.ranks[head_a] < self.ranks[head_b]:
            head_a, head_b = head_b, head_a

        self.parents[head_b] = head_a

        if self.ranks[head_a] == self.ranks[head_b]:
            self.ranks[head_a] += 1

def main():
    # Read in input
    N = int(input()) # Number of lines of input
    m = int(input()) # Number of islands

    dsforrest = DisjointSetForrest(m)

    for line in sys.stdin:
        fields = line.split()
        line_type = fields[0]
        first_island = int(fields[1])
        second_island = int(fields[2])

        if line_type == "B":
            print("Building {} {}".format(first_island, second_island))
            dsforrest.merge(first_island, second_island)
        elif line_type == "Q":
            print("Querying {} {}".format(first_island, second_island))
            if dsforrest.find(first_island) == dsforrest.find(second_island):
                print("Result: y")
            else:
                print("Result: n")
        else:
            print("Error: Unknown command type")

if __name__ == "__main__":
    main()
