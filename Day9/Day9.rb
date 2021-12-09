#!/usr/bin/ruby
# frozen_string_literal: true

filename = (ARGV.empty? ? 'input.txt' : ARGV.first)

def solve(filename)
  lines = File.readlines(filename).map(&:chomp)

  heightmap = parse_heightmap(lines)

  heights = compute_low_points(heightmap)

  total_risk_level = heights.map { |h| h + 1 }.sum

  puts "Part 1: #{total_risk_level}"
end

def parse_heightmap(lines)
  heightmap = []
  lines.each do |line|
    row = []
    line.split('').map(&:to_i).each do |height|
      row << height
    end
    heightmap << row
  end
  heightmap
end

def compute_low_points(heightmap)
  heights = []
  heightmap.each_with_index do |row, r|
    row.each_with_index do |height, c|
      heights << height if low_point?([r, c], heightmap)
    end
  end
  heights
end

def low_point?(position, heightmap)
  r, c = position
  height = heightmap[r][c]
  lower_than_above = (r.positive? ? height < heightmap[r - 1][c] : true)
  lower_than_below = (r < heightmap.length - 1 ? height < heightmap[r + 1][c] : true)
  lower_than_left = (c.positive? ? height < heightmap[r][c - 1] : true)
  lower_than_right = (c < heightmap.first.length - 1 ? height < heightmap[r][c + 1] : true)
  lower_than_above && lower_than_below && lower_than_left && lower_than_right
end

if __FILE__ == $PROGRAM_NAME
  require 'benchmark'
  puts "Input file: #{filename}"
  time = Benchmark.realtime { solve(filename) }
  puts "solve(#{filename}) took #{time} seconds..."
end
