#!/bin/python3
import sys
filename = sys.argv[1] if len(sys.argv) > 1 else "input.txt"

def solve(filename):
  with open(filename) as file:
    lines = file.readlines()

    position = 0
    depth = 0
    aim = 0
    depth2 = 0

    for line in lines:
      direction, x = line.split()
      amount = int(x)

      if direction == "forward":
        position += amount
        depth2 += (aim * amount)
      elif direction == "down":
        depth += amount
        aim += amount
      elif direction == "up":
        depth -= amount
        aim -= amount

    print(f"Part 1: {position * depth}")
    print(f"Part 1: {position * depth2}")

if __name__ == '__main__':
  print(f"Input file: {filename}")
  import time
  start = time.time()
  solve(filename)
  end = time.time()
  print(f"Solve time: {end-start} seconds")
