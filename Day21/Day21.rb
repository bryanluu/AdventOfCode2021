#!/usr/bin/ruby
# frozen_string_literal: true

require './regular_game'
require './quantum_game'

filename = (ARGV.empty? ? 'input.txt' : ARGV.first)

def solve(filename)
  lines = File.readlines(filename).map(&:chomp)
  game1 = RegularGame.new(lines)
  puts "Part 1: #{game1.play}"
  game2 = QuantumGame.new(lines)
  puts game2.play
end

if __FILE__ == $PROGRAM_NAME
  require 'benchmark'
  puts "Input file: #{filename}"
  time = Benchmark.realtime { solve(filename) }
  puts "solve(#{filename}) took #{time} seconds..."
end
