"""
Reads in the grid from raw cases, runs both the Python
and haskell versions and checks the times to ensure that
everythig is fast enough.
"""

import os
import time
import subprocess

raw_dir = "./raw_cases"
out_dir = "./test_cases"

def main():
    errors = 0
    for file_name in os.listdir(raw_dir):
        f = open(os.path.join([raw_dir, file_name]), "r")
        print("Porcessing {}...".format(file_name))
        
        # Run the python version of the script
        start_time = time.time()
        with subprocess.Popen(["src/python/solve.py"], stdin = f, stdout=subprocess.PIPE) as p:
            try:
                p.wait(timeout=10)
            except TimeoutError:
                print("Error: timed out. Test case not genrated")
                errors += 1
                f.close()
                continue
            f.close()
            python_time = time.time() - start_time
            print("Python time: {}".format(python_time))
            if python_time > 7.0: 
                errors += 1
                print("Error: took too long. Test case not genrated")
            output = p.stdout.read()

                

if __name__ == "__main__":
    main()
