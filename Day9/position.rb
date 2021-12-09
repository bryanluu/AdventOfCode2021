class Position
  attr_reader :row, :column, :height

  def initialize(row, column, height)
    @row = row
    @column = column
    @height = height
    @neighbors = []
    @visited = false
  end

  def find_neighbors(heightmap)
    r = row
    c = column
    above = (row.positive? ? heightmap[r - 1][c] : nil)
    below = (row < heightmap.length - 1 ? heightmap[r + 1][c] : nil)
    left = (column.positive? ? heightmap[r][c - 1] : nil)
    right = (column < heightmap.first.length - 1 ? heightmap[r][c + 1] : nil)
    @neighbors << above unless above.nil?
    @neighbors << below unless below.nil?
    @neighbors << left unless left.nil?
    @neighbors << right unless right.nil?
    nil
  end

  def low_point?
    @neighbors.all? { |neighbor| height < neighbor.height }
  end
end
