#!/usr/bin/ruby
# frozen_string_literal: true

filename = (ARGV.empty? ? 'input.txt' : ARGV.first)

def solve(filename)
  lines = File.readlines(filename).map(&:chomp)

  starting_fish = lines.first.split(',').map(&:to_i)

  fish = Hash.new(0)
  starting_fish.each do |f|
    fish[f] += 1
  end

  n_days = 256

  (1..n_days).each do |day|
    lives = fish.keys.sort
    lives.each do |days_left|
      fish[days_left - 1] = fish.delete(days_left)
    end
    fish[6] += fish[-1]
    fish[8] = fish[-1]
    fish.delete(-1)

    puts "Part 1: #{fish.values.sum}" if day == 80
  end

  puts "Part 2: #{fish.values.sum}"
end

if __FILE__ == $PROGRAM_NAME
  require 'benchmark'
  puts "Input file: #{filename}"
  time = Benchmark.realtime { solve(filename) }
  puts "solve(#{filename}) took #{time} seconds..."
end
