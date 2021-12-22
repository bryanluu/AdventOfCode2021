require 'set'
require File.join(File.dirname(__FILE__), '..', 'Tools', 'vector3D')

class Scanner
  DISTANCE_LIMIT = 1000

  attr_reader :label, :number, :beacons, :position

  def initialize(scanner_input)
    parse_label(scanner_input[0])
    parse_beacons(scanner_input[1..])
    @position = Vector3D.zero
  end

  def to_s
    output = "#{@label}\n"
    @beacons.each do |beacon|
      output += "#{beacon}\n"
    end
    output
  end

  def rotate_clockwise_90!(axis)
    axes = { x: 0, y: 1, z: 2 }
    return self unless axes.key?(axis)

    i = axes[axis]
    j = (i + 1) % 3
    k = (i + 2) % 3
    @beacons.each do |beacon|
      pos = beacon.data
      pos[j], pos[k] = -pos[k], pos[j]
    end
    self
  end

  def align_beacons!(origin_scanner)
    offset = find_overlap!(origin_scanner)
    return [] if offset.nil?

    @position = offset
    aligned_beacons = beacons.map do |beacon|
      beacon + @position
    end
    @beacons = Set.new(aligned_beacons)
  end

  def add_beacons!(new_beacons)
    @beacons |= new_beacons
  end

  private

  def parse_label(label_line)
    @label = label_line
    @number = label_line.tr('- scaner', '').to_i
  end

  def parse_beacons(input)
    @beacons = Set.new
    input.each do |line|
      position = line.split(',').map(&:to_i)
      beacon = Vector3D.new(*position)
      @beacons << beacon unless beacon.to_a.any? { |x| x > DISTANCE_LIMIT }
    end
    @beacons
  end

  def overlapping_offset(origin_scanner)
    origin_scanner.beacons.each do |s_beacon|
      beacons.each do |beacon|
        offset = s_beacon - beacon
        overlap = beacons.count { |pos| origin_scanner.beacons.include?(pos + offset) }
        return offset if overlap >= 12
      end
    end
    nil
  end

  def find_overlap!(origin_scanner)
    4.times do
      offset = check_x_face(origin_scanner)
      return offset if offset

      rotate_clockwise_90!(:y)
    end

    rotate_clockwise_90!(:z)
    offset = check_x_face(origin_scanner)
    return offset if offset

    rotate_clockwise_90!(:z)
    rotate_clockwise_90!(:z)
    offset = check_x_face(origin_scanner)
    return offset if offset

    nil
  end

  def check_x_face(origin_scanner)
    4.times do
      rotate_clockwise_90!(:x)
      offset = overlapping_offset(origin_scanner)
      return offset if offset
    end
    nil
  end
end
