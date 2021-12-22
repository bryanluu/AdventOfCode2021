#!/usr/bin/ruby
# frozen_string_literal: true
require './scanner'

filename = (ARGV.empty? ? 'input.txt' : ARGV.first)

def solve(filename)
  lines = File.readlines(filename)
  scanner_input = lines.join.split("\n\n").map { |scanner_lines| scanner_lines.split("\n").map(&:chomp) }
  scanners = []
  scanner_input.each do |input|
    scanner = Scanner.new(input)
    scanners << scanner
  end

  origin = scanners[0]
  unplaced_scanners = scanners[1..]
  until unplaced_scanners.empty?
    scanner = unplaced_scanners.shift
    overlapping_beacons = scanner.align_beacons!(origin)
    if overlapping_beacons.empty?
      unplaced_scanners << scanner
    else
      origin.add_beacons!(overlapping_beacons)
    end
  end

  max_distance = nil
  scanners.each_with_index do |scanner1, i|
    scanners.each_with_index do |scanner2, j|
      next if i == j

      manhattan_distance = (scanner1.position - scanner2.position).to_a.map(&:abs).sum
      max_distance = manhattan_distance if max_distance.nil? || manhattan_distance > max_distance
    end
  end

  puts "Part 1: #{origin.beacons.length}"
  puts "Part 2: #{max_distance}"
end

if __FILE__ == $PROGRAM_NAME
  require 'benchmark'
  puts "Input file: #{filename}"
  time = Benchmark.realtime { solve(filename) }
  puts "solve(#{filename}) took #{time} seconds..."
end
