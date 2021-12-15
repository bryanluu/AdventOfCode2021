class RiskNode
  attr_reader :row, :column, :risk, :edges
  attr_accessor :visited, :distance

  def initialize(row, column, risk_level)
    @row = row
    @column = column
    @risk = risk_level
    @edges = {}
    @distance = (row.zero? && column.zero? ? 0 : nil)
    @visited = false
  end

  def id
    "#{row},#{column}"
  end

  def connect_to(other)
    return if @edges.key?(other.id)

    @edges[other.id] = other.risk
    other.connect_to(self)
  end

  def to_s
    "<#{id}: #{@edges.inspect}>"
  end
end
