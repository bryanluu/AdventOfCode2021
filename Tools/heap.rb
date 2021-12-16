class Heap
  def initialize(data = [], &comparator)
    @data = data
    @comparator = (block_given? ? comparator : proc { |x, y| x < y })
  end

  def insert!(value); end

  def extract!; end

  def root
    @data[0]
  end

  def size
    @data.length
  end

  def data
    @data.clone
  end
end
