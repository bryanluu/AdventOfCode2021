#!/usr/bin/ruby
# frozen_string_literal: true

require './network'
require 'pry'

filename = (ARGV.empty? ? 'input.txt' : ARGV.first)

def solve(filename)
  lines = File.readlines(filename).map(&:chomp)

  network = Network.new(lines)
  network.explore_routes('start', 'end')

  puts "Part 1: #{network.routes.length}"
end

if __FILE__ == $PROGRAM_NAME
  require 'benchmark'
  puts "Input file: #{filename}"
  time = Benchmark.realtime { solve(filename) }
  puts "solve(#{filename}) took #{time} seconds..."
end
