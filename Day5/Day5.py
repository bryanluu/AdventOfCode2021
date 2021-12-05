#!/bin/python3
import sys
from collections import defaultdict as dd
filename = sys.argv[1] if len(sys.argv) > 1 else "input.txt"

def solve(filename):
  with open(filename) as file:
    lines = file.readlines()

    vents1 = dd(lambda: 0)
    vents2 = dd(lambda: 0)

    for line in lines:
      start, end = line.split(' -> ')
      x1, y1 = parseCoordinates(start)
      x2, y2 = parseCoordinates(end)
      lx, ux = order(x1, x2)
      ly, uy = order(y1, y2)
      if isStraight((x1, y1), (x2, y2)):
        for x in range(lx, ux + 1):
          for y in range(ly, uy + 1):
            vents1[(x, y)] += 1
            vents2[(x, y)] += 1
      else:
        for i in range(ux - lx + 1):
        if isDiagonal((x1, y1), (x2, y2)):
            vents2[(lx + i, ly + i)] += 1
        else:
            vents2[(lx + i, uy - i)] += 1

    part1 = len([count for count in vents1.values() if count >= 2])
    part2 = len([count for count in vents2.values() if count >= 2])

    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")

def parseCoordinates(coord):
  x, y = map(int, coord.split(','))
  return x, y

def isStraight(start, end):
  x1, y1 = start
  x2, y2 = end
  return x1 == x2 or y1 == y2

def order(a, b):
  if a == b:
    return a, b

  sm = (a if a < b else b)
  lg = (a if a > b else b)
  return sm, lg

def isDiagonal(start, end):
  x1, y1 = start
  x2, y2 = end
  return (x2 - x1) == (y2 - y1)

if __name__ == '__main__':
  print(f"Input file: {filename}")
  import time
  start = time.time()
  solve(filename)
  end = time.time()
  print(f"Solve time: {end-start} seconds")
