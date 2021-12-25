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
  pdb.set_trace()
  if power_on:
    leftover = calculate_excluded_cubes(cuboid, on_cuboids)
    on_cuboids |= leftover
  else:
    turn_off_colliding_cuboids(cuboid, on_cuboids)

def turn_off_colliding_cuboids(cuboid, other_cuboids):
  processed = set()
  while len(other_cuboids) > 0:
    other_cuboid = other_cuboids.pop()
    if cuboid.collides_with(other_cuboid):
      other_cuboids |= (other_cuboid - cuboid)
    else:
      processed.add(cuboid)
  other_cuboids |= processed

def calculate_excluded_cubes(cuboid, other_cuboids):
  cuboids = set([cuboid])
  processed = set()
  while len(other_cuboids) > 0:
    other_cuboid = other_cuboids.pop()
    exclusive = set()
    broke = False
    while len(cuboids) > 0:
      cuboid = cuboids.pop()
      if cuboid.collides_with(other_cuboid):
        exclusive.discard(cuboid)
        cuboid_exclusive = (cuboid - other_cuboid)
        other_cuboid_exclusive = (other_cuboid - cuboid)
        processed.discard(other_cuboid_exclusive)
        cuboids |= cuboid_exclusive
        processed |= other_cuboid_exclusive
        broke = True
      else:
        exclusive.add(cuboid)
    cuboids = exclusive
    if not broke:
      processed.add(other_cuboid)
  other_cuboids |= processed

  return cuboids

def count_cubes_that_are_on(on_cuboids):
  print(on_cuboids)
  return sum(cuboid.cubes() for cuboid in on_cuboids)

if __name__ == '__main__':
  print(f"Input file: {filename}")
  import time
  start = time.time()
  solve(filename)
  end = time.time()
  print(f"Solve time: {end-start} seconds")
