#!/bin/python3
import sys
from collections import defaultdict as dd
filename = sys.argv[1] if len(sys.argv) > 1 else "input.txt"

def solve(filename):
  with open(filename) as file:
    lines = file.readlines()
    template = lines[0].strip()
    rules = parse_rules(lines[2:])
    polymer = template

    print(f"Template: {template}")
    count = {}
    for step in range(10):
      polymer, count = process_polymer(polymer, rules)
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
  for line in lines:
    pair, code = line.strip().split(' -> ')
    rules[pair] = code
  return rules

def process_polymer(polymer, rules):
  result = []
  count = dd(lambda: 0)
  for i in range(len(polymer) - 1):
    pair = polymer[i:i+2]
    if i == 0:
      result.append(pair[0])
      count[pair[0]] += 1
    if pair in rules:
      result.append(rules[pair])
      count[rules[pair]] += 1
    result.append(pair[1])
    count[pair[1]] += 1
  new_polymer = "".join(result)
  return new_polymer, count

if __name__ == '__main__':
  print(f"Input file: {filename}")
  import time
  start = time.time()
  solve(filename)
  end = time.time()
  print(f"Solve time: {end-start} seconds")
