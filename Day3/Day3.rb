#!/usr/bin/ruby
# frozen_string_literal: true

filename = (ARGV.empty? ? 'input.txt' : ARGV.first)

def solve(filename)
  lines = File.readlines(filename).map(&:chomp)
  n = lines.first.length
  ones = [0] * n
  gamma = 'x' * n
  epsilon = 'y' * n

  lines.each do |line|
    line.split('').each_with_index do |x, i|
      ones[i] += x.to_i
    end
  end

  ones.each_with_index do |count, i|
    gamma[i] = (count > lines.length - count ? '1' : '0')
    epsilon[i] = (gamma[i] == '1' ? '0' : '1')
  end

  oxygen_generator_rating = get_rating(lines, 0, oxygen: true)
  co2_scrubber_rating = get_rating(lines, 0, oxygen: false)

  puts "Part 1: Gamma: #{gamma}, Epsilon: #{epsilon}, Solution: #{gamma.to_i(2) * epsilon.to_i(2)}"
  puts "Part 2: O2: #{oxygen_generator_rating}, CO2: #{co2_scrubber_rating}, Solution: #{oxygen_generator_rating.to_i(2) * co2_scrubber_rating.to_i(2)}"
end

def get_rating(lines, position, oxygen: true)
  return lines.first if lines.length == 1

  n = lines.first.length
  ones = [0] * n
  lines.each do |line|
    x = line[position]
    ones[position] += x.to_i
  end

  t = (oxygen ? '1' : '0')
  f = (oxygen ? '0' : '1')
  target = (ones[position] >= lines.length - ones[position] ? t : f)

  new_lines = lines.filter { |line| line[position] == target }

  get_rating(new_lines, position + 1, oxygen: oxygen)
end

if __FILE__ == $PROGRAM_NAME
  require 'benchmark'
  puts "Input file: #{filename}"
  time = Benchmark.realtime { solve(filename) }
  puts "solve(#{filename}) took #{time} seconds..."
end
