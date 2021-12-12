#!/usr/bin/ruby
# frozen_string_literal: true

require './network'
require 'pry'

filename = (ARGV.empty? ? 'input.txt' : ARGV.first)

def solve(filename)
  lines = File.readlines(filename).map(&:chomp)

  network = Network.new(lines)
  routes_part1 = network.find_routes
  routes_part2 = network.find_modified_routes

  puts "Part 1: #{routes_part1.length}"
  puts "Part 2: #{routes_part2.length}"
end

if __FILE__ == $PROGRAM_NAME
  require 'benchmark'
  puts "Input file: #{filename}"
  time = Benchmark.realtime { solve(filename) }
  puts "solve(#{filename}) took #{time} seconds..."
end
