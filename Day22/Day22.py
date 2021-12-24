#!/bin/python3
import sys
import numpy as np

filename = sys.argv[1] if len(sys.argv) > 1 else "input.txt"

INITIALIZATION_REGION_SIZE = 101

def solve(filename):
  with open(filename) as file:
    lines = file.readlines()
    cubes = np.zeros(shape=[101, 101, 101], dtype=bool)
    for line in lines:
      cuboid, power_on = parse_cuboid(line)
      reboot_cubes(cubes, cuboid, power_on)
    print(f"Part 1: {cubes[0:101, 0:101, 0:101].sum()}")

def parse_cuboid(line):
  power_on = line.startswith('on')
  range_strings = line.strip('onf').split(',')
  cuboid = [parse_range(range_str) for range_str in range_strings]
  return cuboid, power_on

def parse_range(range_str):
  _, coord_str = range_str.split('=')
  low, high = map(int, coord_str.split('..'))
  return low, high

def reboot_cubes(cubes, cuboid, power_on):
  (low_x, high_x), (low_y, high_y), (low_z, high_z) = translated_coordinates(cubes, cuboid)
  cubes[low_x:high_x, low_y:high_y, low_z:high_z] = power_on

def translated_coordinates(cubes, cuboid):
  (low_x, high_x), (low_y, high_y), (low_z, high_z) = cuboid
  width, height, depth = cubes.shape
  x_offset, y_offset, z_offset = width//2, height//2, depth//2
  return (low_x + x_offset, high_x + x_offset + 1), (low_y + y_offset, high_y + y_offset + 1), (low_z + z_offset, high_z + z_offset + 1)

def cubes(cubes, cuboid):
  pass

if __name__ == '__main__':
  print(f"Input file: {filename}")
  import time
  start = time.time()
  solve(filename)
  end = time.time()
  print(f"Solve time: {end-start} seconds")
