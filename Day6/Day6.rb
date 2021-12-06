#!/usr/bin/ruby
# frozen_string_literal: true

filename = (ARGV.empty? ? 'input.txt' : ARGV.first)

def solve(filename)
  lines = File.readlines(filename).map(&:chomp)

  fish = lines.first.split(',').map(&:to_i)

  80.times do |day|
    (0...fish.length).each do |i|
      if fish[i].zero?
        fish.push(8) if fish[i].zero?
        fish[i] = 6
      else
        fish[i] -= 1
      end
    end
  end

  puts "Part 1: #{fish.length}"
end

if __FILE__ == $PROGRAM_NAME
  require 'benchmark'
  puts "Input file: #{filename}"
  time = Benchmark.realtime { solve(filename) }
  puts "solve(#{filename}) took #{time} seconds..."
end
