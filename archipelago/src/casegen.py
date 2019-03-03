#!/usr/bin/python3

import argparse, random
from subprocess import Popen

def generate_case(num_islands, num_lines, rng):
    """Returns string of test case file based on parameters"""
    out_string = "{}\n{}\n".format(num_lines, num_islands)

    bridges = set()
    for i in range(num_lines):        
        #print("line_number={}".format(i))
        building_bridge = False
        if rng.random() < 0.5: # Build a bridge
            building_bridge = True
            while True:
                first = rng.randrange(0, num_islands)
                second = rng.randrange(0, num_islands)
                if first == second:
                    continue
                if second < first:
                    first, second = second, first
                if (first, second) in bridges:
                    building_bridge = False
                break
            if building_bridge:
                bridges.add((first, second))
                if rng.random() < 0.5: # Randomize order
                    out_string += "B {} {}\n".format(first, second)
                else:
                    out_string += "B {} {}\n".format(second, first)
        if not building_bridge: # Make a query
            while True:
                first = rng.randrange(0, num_islands)
                second = rng.randrange(0, num_islands)
                if first == second:
                    continue
                break
            out_string += "Q {} {}\n".format(first, second)
    return out_string


def main():
    # Read the command-line arguments
    parser = argparse.ArgumentParser(description="Generate test cases for archipelago problem.")
    parser.add_argument("case_file", help="Name of the test case file.")
    parser.add_argument("sol_file", help="Name of the solution file.")
    parser.add_argument("num_islands", type=int, help="Number of islands in the problem.")
    parser.add_argument("num_lines", type=int, help="Number of builds/queries")
    parser.add_argument("seed", type=int, help="Random number generator seed")
    args = parser.parse_args()

    rng = random.Random(args.seed)
    out_string = generate_case(args.num_islands, args.num_lines, rng)

    with open(args.case_file, "w") as case_file:
        case_file.write(out_string)

    # Generate the solution file using the cpp solution
    #print("Finding solution...")
    with open(args.case_file, "r") as case_file, \
         open(args.sol_file, "w") as sol_file, \
         Popen("./archipelago", 
               stdin=case_file,
               stdout=sol_file) as p:
        p.wait()

if __name__ == "__main__":
    main()
