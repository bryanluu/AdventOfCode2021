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

      decoding = decode_digits(segment_map)

      print(f"{input_values}: {decoding}")

      for code in output_values:
        if len(code) in digit_map:
          count += 1

    print(f"Part 1: {count}")

def decode_digits(segment_map):
  decoding = { code: digit for digit, code in segment_map.items() if digit != 'leftovers' }
  segments = { digit: set(segment_map[digit]) for digit in segment_map.keys() }
  # decode each digit
  for code in segment_map['leftovers']:
    if len(code) == 6:
      if not segments[1] <= set(code):
        digit = 6
      else:
        symm_diff = set(code) ^ segments[8]
        if symm_diff <= segments[4]:
          digit = 0
        else:
          digit = 9
    if len(code) == 5:
      if segments[1] <= set(code):
        digit = 3
      else:
        symm_diff = set(code) ^ segments[4]
        if len(symm_diff) == 3:
          digit = 5
        else:
          digit = 2
    decode_digit(digit, code, decoding)
  return decoding

def decode_digit(digit, code, decoding):
  decoding[code] = digit

if __name__ == '__main__':
  print(f"Input file: {filename}")
  import time
  start = time.time()
  solve(filename)
  end = time.time()
  print(f"Solve time: {end-start} seconds")
