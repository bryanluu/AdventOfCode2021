#!/bin/python3
import sys
from collections import defaultdict as dd
filename = sys.argv[1] if len(sys.argv) > 1 else "input.txt"

def solve(filename):
  with open(filename) as file:
    lines = file.readlines()
    template = lines[0].strip()
    rules, tree = parse_rules(lines[2:])
    polymer = template

    print(f"Template: {template}")
    pairs = process(polymer, tree, 40)
    count = count_characters(polymer, pairs)
    max_letter = None
    min_letter = None
    for code in count.keys():
      if max_letter is None or count[code] > count[max_letter]:
        max_letter = code
      if min_letter is None or count[code] < count[min_letter]:
        min_letter = code
    print(f"Part 1: {count[max_letter] - count[min_letter]}")

def parse_rules(lines):
  rules = {}
  tree = {}
  for line in lines:
    pair, code = line.strip().split(' -> ')
    rules[pair] = code
    tree[pair] = {pair[0] + code, code + pair[1]}
  return rules, tree

def process(polymer, tree, steps):
  count = dd(lambda: 0)
  for i in range(len(polymer) - 1):
    pair = polymer[i:i+2]
    count[pair] += 1
  for step in range(steps):
    next_count = dd(lambda: 0)
    for pair in count.keys():
      for child in tree[pair]:
        next_count[child] += count[pair]
    count = next_count.copy()
  return count

def count_characters(polymer, pairs):
  count = dd(lambda: 0)
  count[polymer[0]] = 1
  for pair in pairs.keys():
    code = pair[1]
    count[code] += pairs[pair]
  return count

if __name__ == '__main__':
  print(f"Input file: {filename}")
  import time
  start = time.time()
  solve(filename)
  end = time.time()
  print(f"Solve time: {end-start} seconds")
