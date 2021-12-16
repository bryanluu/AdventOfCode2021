require './risk_map'

class BigRiskMap < RiskMap
  def initialize(lines)
    super(lines)
  end

  private

  def populate_map(lines)
    hypermap = []
    (0...5).each do |mr|
      meta_row = []
      (0...5).each do |mc|
        grid = lines.map do |line|
          line.split('').map { |x| (x.to_i + mc + mr - 1) % 9 + 1 }.join
        end
        meta_row << grid
      end
      hypermap << meta_row
    end
    super(flattened_hypermap(hypermap))
  end

  def flattened_hypermap(hypermap)
    lines = []
    hypermap.each do |hyper_row|
      lines << hyper_row.reduce do |memo, map|
        memo.each_with_index.map { |row, r| row + map[r] }
      end
    end
    lines.flatten!
  end
end
