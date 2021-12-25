#!/bin/python3
import sys
from cuboid import Cuboid
import pdb

filename = sys.argv[1] if len(sys.argv) > 1 else "input.txt"

INITIALIZATION_REGION_SIZE = 101

def solve(filename):
  with open(filename) as file:
    lines = file.readlines()
    on_cuboids = set()
    for line in lines:
      cuboid, power_on = parse_cuboid(line)
      reboot_cubes(on_cuboids, cuboid, power_on)
    print(f"Cubes: {count_cubes_that_are_on(on_cuboids)}")

def parse_cuboid(line):
  power_on = line.startswith('on')
  range_strings = line.strip('onf').split(',')
  cuboid = Cuboid(tuple(parse_range(range_str) for range_str in range_strings))
  return cuboid, power_on

def parse_range(range_str):
  _, coord_str = range_str.split('=')
  low, high = map(int, coord_str.split('..'))
  return low, high

def reboot_cubes(on_cuboids, cuboid, power_on):
  if power_on:
    on_cuboids |= cuboid.combine_to_cuboids(on_cuboids)
  else:
    cuboid.remove_colliding_cuboids(on_cuboids)

def count_cubes_that_are_on(on_cuboids):
  return sum(cuboid.cubes() for cuboid in on_cuboids)

if __name__ == '__main__':
  print(f"Input file: {filename}")
  import time
  start = time.time()
  solve(filename)
  end = time.time()
  print(f"Solve time: {end-start} seconds")
