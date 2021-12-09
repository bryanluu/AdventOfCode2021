class Basin
  attr_reader :size

  def initialize(position)
    @visited = Hash.new(false)
    @included = Hash.new(false)
    @visited[key_for(position)] = true
    @included[key_for(position)] = true
    @size = 1
    @root = position
  end

  def measure
    puts "--- #{key_for(@root)}: #{@root.height} ---"
    @root.neighbors.each do |target|
      build_basin(@root, target)
    end
    puts "basin: #{@included.keys.inspect}"
  end

  private

  def key_for(position)
    [position.row, position.column]
  end

  def build_basin(src, target, level: 0)
    # peform a DFS on the target node, keeping track of the source node
    return if @included[key_for(target)]
    return if target.height == 9
    return if target.height - src.height > 1
    return if (target.height - src.height).negative?

    @included[key_for(target)] = true
    @size += 1
    puts '   ' * level + "add #{key_for(target).inspect}: #{target.height} to basin"

    target.neighbors.each do |neighbor|
      build_basin(target, neighbor, level: level + 1)
    end
  end
end
