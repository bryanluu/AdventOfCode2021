class Cave
  attr_reader :label, :neighbors

  def initialize(label)
    @label = label
    @neighbors = []
  end

  def connect_to(other)
    return if @neighbors.include?(other)

    @neighbors << other
    other.connect_to(self)
  end

  def to_s
    "<#{label}: #{neighbors.map(&:label)}>"
  end

  def big?
    @big ||= (@label.upcase == @label)
  end
end
