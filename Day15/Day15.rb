#!/usr/bin/ruby
# frozen_string_literal: true

require './risk_map'
require './big_risk_map'

filename = (ARGV.empty? ? 'input.txt' : ARGV.first)

def solve(filename)
  lines = File.readlines(filename).map(&:chomp)

  risk_map = RiskMap.new(lines)
  risk_map.find_shortest_path
  big_risk_map = BigRiskMap.new(lines)
  big_risk_map.find_shortest_path

  puts "Part 1: #{risk_map.total_risk}"
  puts "Part 2: #{big_risk_map.total_risk}"
end

if __FILE__ == $PROGRAM_NAME
  require 'benchmark'
  puts "Input file: #{filename}"
  time = Benchmark.realtime { solve(filename) }
  puts "solve(#{filename}) took #{time} seconds..."
end
