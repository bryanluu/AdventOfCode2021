#!/bin/python3
import sys
import math
filename = sys.argv[1] if len(sys.argv) > 1 else "input.txt"

def solve(filename):
  with open(filename) as file:
    input_line = file.readline().strip()
    area_info = input_line.removeprefix('target area: ')
    target_area = parse_target_area(area_info)
    print(f"Part 1: {max_peak_height(target_area)}")
    print(f"Part 2: {len(find_possible_velocities(target_area))}")

def parse_target_area(info):
  x_info, y_info = info.split(", ")
  x1, x2 = parse_coordinates(x_info)
  y1, y2 = parse_coordinates(y_info)
  return (x1, y1), (x2, y2)

def parse_coordinates(info):
  _, coords = info.split('=')
  a, b = coords.split('..')
  return int(a), int(b)

def min_x_speed(target_area):
  (lx, ly), (ux, uy) = target_area
  # found by solving the recurrence relations
  # x(n) = x(n-1) + vx(n-1)
  # vx(n) = vx(n-1) - 1
  return math.ceil((math.sqrt(1 + 8*lx) - 1)/2)

def max_peak_height(target_area):
  (lx, ly), (ux, uy) = target_area
  # the probe travels in a parabola, inspired by Reddit user Bergdublone's solution
  # at max y_speed, the probe barely makes the target area, so the negative speed at this point is the difference between the two heights
  vy = ly
  y = ly
  while vy != 0:
    # climb the parabola backwards until the peak is reached
    y -= vy
    vy += 1
  # return the height of the peak
  return y

def find_possible_velocities(target_area):
  (x1, y1), (x2, y2) = target_area
  min_vx = min_x_speed(target_area)
  max_vy = -(y1 + 1)
  successful = []
  for vx in range(min_vx, x2+1):
    for vy in range(y1, max_vy+1):
      hit = test_trajectory((vx, vy), target_area)
      if hit:
        successful.append((vx, vy))
  return successful

def test_trajectory(initial_velocity, target_area):
  (x1, y1), (x2, y2) = target_area
  x, y = 0, 0
  vx, vy = initial_velocity
  while x <= x2 and y >= y1:
    (x, y), (vx, vy) = step((x, y), (vx, vy))
    if x1 <= x <= x2 and y1 <= y <= y2:
      return True
  return False

def step(position, velocity):
  x, y = position
  vx, vy = velocity
  x += vx
  y += vy
  if vx != 0:
    vx -= sign(vx)
  vy -= 1
  return (x, y), (vx, vy)

def sign(x):
  return 1 if x >= 0 else -1

if __name__ == '__main__':
  print(f"Input file: {filename}")
  import time
  start = time.time()
  solve(filename)
  end = time.time()
  print(f"Solve time: {end-start} seconds")
