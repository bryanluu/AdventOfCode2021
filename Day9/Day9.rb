#!/usr/bin/ruby
# frozen_string_literal: true

require './position'
require './basin'
require 'pry'

filename = (ARGV.empty? ? 'input.txt' : ARGV.first)

def solve(filename)
  lines = File.readlines(filename).map(&:chomp)

  heightmap = parse_heightmap(lines)
  low_points = compute_low_points(heightmap)
  total_risk_level = low_points.map { |pos| pos.height + 1 }.sum
  basin_sizes = measure_basins(low_points)
  basin_product = basin_sizes.sort[-3..].reduce(:*)

  puts "Part 1: #{total_risk_level}"
  puts "Part 2: #{basin_product}"
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

def measure_basins(low_points)
  basin_sizes = []
  low_points.each do |position|
    basin = Basin.new(position)
    basin.measure
    basin_sizes << basin.size
  end
  basin_sizes
end

if __FILE__ == $PROGRAM_NAME
  require 'benchmark'
  puts "Input file: #{filename}"
  time = Benchmark.realtime { solve(filename) }
  puts "solve(#{filename}) took #{time} seconds..."
end
