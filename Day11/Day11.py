#!/bin/python3
import sys
from octopus import Octopus

filename = sys.argv[1] if len(sys.argv) > 1 else "input.txt"

def solve(filename):
  with open(filename) as file:
    lines = file.readlines()

    Octopus.populate(lines)
    Octopus.connect()

    print("--- Starting ---")
    Octopus.display()

    N = 100000
    total_flashes = 0
    sync_step = 0
    synced = False
    for step in range(1, N+1):
      print(f"--- Step {step} ---")
      flashes = Octopus.step()
      Octopus.display()
      if step <= 100:
        total_flashes += flashes
      if (not synced and Octopus.are_synchronized()):
        sync_step = step
        synced = True
        if step > 100:
          break

    print(f"Part 1: {total_flashes}")
    print(f"Part 2: {sync_step}")

if __name__ == '__main__':
  print(f"Input file: {filename}")
  import time
  start = time.time()
  solve(filename)
  end = time.time()
  print(f"Solve time: {end-start} seconds")
