#!/usr/bin/ruby
# frozen_string_literal: true

require './position'

filename = (ARGV.empty? ? 'input.txt' : ARGV.first)

def solve(filename)
  lines = File.readlines(filename).map(&:chomp)

  heightmap = parse_heightmap(lines)

  heights = compute_low_points(heightmap)

  total_risk_level = heights.map { |h| h.height + 1 }.sum

  puts "Part 1: #{total_risk_level}"
end

def parse_heightmap(lines)
  heightmap = []
  lines.each_with_index do |line, r|
    row = []
    line.split('').map(&:to_i).each_with_index do |height, c|
      position = Position.new(r, c, height)
      row << position
    end
    heightmap << row
  end
  heightmap
end

def compute_low_points(heightmap)
  heights = []
  heightmap.each do |row|
    row.each do |position|
      position.find_neighbors(heightmap)
      heights << position if position.low_point?
    end
  end
  heights
end

if __FILE__ == $PROGRAM_NAME
  require 'benchmark'
  puts "Input file: #{filename}"
  time = Benchmark.realtime { solve(filename) }
  puts "solve(#{filename}) took #{time} seconds..."
end
