require './risk_node'
require 'set'

class RiskMap
  def initialize(lines)
    @nodes = {}
    @positions = []
    populate_map(lines)
    @unvisited = Set.new(@nodes.keys)
    @shortest_path = []
  end

  def find_shortest_path
    curr = @start
    prev = {}

    until curr.id == @end.id
      curr.edges.each do |nb, edge|
        neighbor = @nodes[nb]
        next if neighbor.visited

        new_dist = curr.distance + edge
        if neighbor.distance.nil? || new_dist < neighbor.distance
          neighbor.distance = new_dist
          prev[neighbor.id] = curr.id
        end
      end
      curr.visited = true
      @unvisited.delete(curr.id)
      curr = min_distance_node
    end

    @shortest_path.clear
    until prev[curr.id].nil? || curr.id == @start.id
      @shortest_path.prepend(curr)
      curr = @nodes[prev[curr.id]]
    end

    @shortest_path
  end

  def total_risk
    @shortest_path.map(&:risk).sum
  end

  def to_s
    output = ''
    @positions.each do |row|
      row.each do |node|
        if @shortest_path.empty?
          output += node.risk.to_s
        else
          output += (@shortest_path.include?(node) ? node.risk.to_s : '.')
        end
      end
      output += "\n"
    end
    output
  end

  private

  def populate_map(lines)
    lines.each_with_index do |line, r|
      row_risk = line.split('').map(&:to_i)
      row = []
      row_risk.each_with_index do |risk, c|
        node = RiskNode.new(r, c, risk)
        up = (r.positive? ? @positions[r - 1][c] : nil)
        left = (c.positive? ? row[c - 1] : nil)
        node.connect_to(up) unless up.nil?
        node.connect_to(left) unless left.nil?
        row << node
        @nodes["#{r},#{c}"] = node
      end
      @positions << row
      @start = @positions[0][0]
      @end = @positions[-1][-1]
    end
  end

  def min_distance_node
    min_node = nil
    @unvisited.each do |pos|
      node = @nodes[pos]
      min_node = node if min_node.nil? || (!node&.distance.nil? && node.distance < min_node.distance)
    end
    min_node
  end
end
