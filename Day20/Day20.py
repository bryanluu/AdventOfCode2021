#!/bin/python3
import sys
from image import Image

filename = sys.argv[1] if len(sys.argv) > 1 else "input.txt"

def solve(filename):
  with open(filename) as file:
    lines = list(map(lambda line: line.strip(), file.readlines()))
    algorithm = lines[0]
    input_grid = list(map(lambda line: [c for c in line], lines[2:]))
    image = Image(input_grid, algorithm)
    part1_answer = None
    for i in range(1, 51):
      image.enhance()
      if i == 2:
        part1_answer = image.lit_pixel_count()
    part2_answer = image.lit_pixel_count()
    print(f"Part 1: {part1_answer}")
    print(f"Part 2: {part2_answer}")

if __name__ == '__main__':
  print(f"Input file: {filename}")
  import time
  start = time.time()
  solve(filename)
  end = time.time()
  print(f"Solve time: {end-start} seconds")
