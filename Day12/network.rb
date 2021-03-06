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
  end

  def find_routes(extra_cave: nil)
    queue = []
    routes = []

    queue << [@caves['start']]

    until queue.empty?
      path = queue.shift
      cave = path.last

      if cave.label == 'end'
        routes << path.map(&:label)
      else
        cave.neighbors.each do |neighbor|
          queue << path + [neighbor] unless visited(neighbor, path, extra_cave: extra_cave)
        end
      end
    end

    routes
  end

  def find_modified_routes
    routes = []
    small_caves = caves.keys.reject do |cave|
      @caves[cave].big? || cave == 'start' || cave == 'end'
    end

    small_caves.each do |cave|
      routes.concat(find_routes(extra_cave: cave))
    end
    routes.uniq
  end

  def to_s
    output = ''
    @caves.each_key do |cave|
      output += "#{@caves[cave]}\n"
    end
    output
  end

  #######
  private
  #######

  def visited(cave, path_so_far, extra_cave: nil)
    return false if cave.big?

    limit = cave.label == extra_cave ? 2 : 1

    path_so_far.find_all do |c|
      c.label == cave.label
    end.count >= limit
  end
end
