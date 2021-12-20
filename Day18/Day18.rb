#!/usr/bin/ruby
# frozen_string_literal: true
require './pair'

filename = (ARGV.empty? ? 'input.txt' : ARGV.first)

def solve(filename)
  lines = File.readlines(filename).map(&:chomp)

  pairs = []
  lines.each do |line|
    pair = Pair.construct_from_string(line)
    pairs << pair
  end

  max_magnitude = nil
  max_result = nil
  pairs.each_with_index do |x, i|
    pairs.each_with_index do |y, j|
      next if i == j

      result = x + y
      mag = result.abs
      if max_magnitude.nil? || mag > max_magnitude
        max_magnitude = mag
        max_result = [x, y]
      end
    end
  end

  puts [max_result[0].to_s, max_result[1].to_s].inspect
  puts max_result[0] + max_result[1]

  part1_result = pairs.reduce(&:+).abs
  part2_result = max_magnitude

  puts "Part 1: #{part1_result}"
  puts "Part 2: #{part2_result}"
end

if __FILE__ == $PROGRAM_NAME
  require 'benchmark'
  puts "Input file: #{filename}"
  time = Benchmark.realtime { solve(filename) }
  puts "solve(#{filename}) took #{time} seconds..."
end
