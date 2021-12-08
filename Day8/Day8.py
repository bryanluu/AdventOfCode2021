#!/bin/python3
import sys
filename = sys.argv[1] if len(sys.argv) > 1 else "input.txt"

def solve(filename):
  with open(filename) as file:
    lines = file.readlines()

    # Map number of segments to unique digits
    digit_map = { 2: 1, 4: 4, 3: 7, 7: 8 }

    count = 0
    for line in lines:
      # sort each code alphabetically before processing
      input_values, output_values = map(lambda x: list(map(lambda y: "".join(sorted(y)), x.strip().split())), line.split('|'))
      # map digit to number of segments
      segment_map = {}

      for code in input_values:
        if len(code) in digit_map:
          segment_map[digit_map[len(code)]] = code
        else:
          segment_map['leftovers'] = segment_map.get('leftovers', [])
          segment_map['leftovers'].append(code)

      decode_digits(segment_map)

      for code in output_values:
        if len(code) in digit_map:
          count += 1

    print(f"Part 1: {count}")

def decode_digits(segment_map):
  mapping = {}
  decoding = { code: digit for digit, code in segment_map.items() if digit != 'leftovers' }
  segments = { digit: set(segment_map[digit]) for digit in segment_map.keys() }
  # decode a
  for a in segments[7] - segments[1]:
    mapping[a] = 'a'
    break
  # decode cdef
  for code in segment_map['leftovers']:
    if len(code) == 6:
      if not segments[1] <= set(code):
        # code is 6
        f = next(iter(segments[1] & set(code)))
        mapping[f] = 'f'
        decoding[code] = 6
        segments[6] = code
        c = next(iter(segments[1]))
        mapping[c] = 'c'
        decoding[segment_map[1]] = 1
      else:
        symm_diff = set(code) ^ segments[8]
        if symm_diff <= segments[4]:
          # code is 9
          digit = 9
          character = 'd'
        else:
          # code is 0
          digit = 0
          character = 'e'
        letter = next(iter(symm_diff))
        mapping[letter] = character
        decoding[code] = digit
        segments[digit] = code
    if len(code) == 5:
      symm_diff = set(code) ^ segments[8]

if __name__ == '__main__':
  print(f"Input file: {filename}")
  import time
  start = time.time()
  solve(filename)
  end = time.time()
  print(f"Solve time: {end-start} seconds")
