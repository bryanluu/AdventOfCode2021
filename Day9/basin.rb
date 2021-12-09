class Basin
  attr_reader :size

  def initialize(position)
    @included = Hash.new(false)
    @size = 0
    @root = position
  end

  def measure
    build_basin(@root)
  end

  private

  def key_for(position)
    [position.row, position.column]
  end

  def build_basin(target, level: 0)
    # peform a DFS on the target node, keeping track of the source node
    return if @included[key_for(target)]
    return if target.height == 9

    @included[key_for(target)] = true
    @size += 1

    target.neighbors.each do |neighbor|
      build_basin(neighbor, level: level + 1)
    end
  end
end
