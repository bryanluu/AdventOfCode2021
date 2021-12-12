require './cave'

class Network
  attr_reader :caves, :routes

  def initialize(lines)
    @caves = Hash.new { |h, key| h[key] = Cave.new(key) }
    lines.each do |line|
      c1, c2 = line.split('-')
      cave1 = @caves[c1]
      cave2 = @caves[c2]
      cave1.connect_to(cave2)
    end
    @routes = []
  end

  def explore_routes(src, dst)
    queue = []

    queue << [@caves[src]]

    until queue.empty?
      path = queue.shift
      cave = path.last

      if cave.label == dst
        @routes << path.map(&:label)
      else
        cave.neighbors.each do |neighbor|
          visited = neighbor.small? && path.include?(neighbor)
          queue << path + [neighbor] unless visited
        end
      end
    end
    @routes
  end

  def to_s
    output = ''
    @caves.each_key do |cave|
      output += "#{@caves[cave]}\n"
    end
    output
  end
end
