class Heap
  def initialize(data = [], &comparator)
    @data = data
    @comparator = (block_given? ? comparator : proc { |x, y| x <=> y })
    heapify!
  end

  def insert!(value)
    @data << value
    percolate_up!(@data.length - 1)
  end

  def extract!
    return nil if @data.empty?

    @data[0], @data[@data.length - 1] = @data[@data.length - 1], @data[0]
    res = @data.pop
    percolate_down!(0)
    res
  end

  def root
    @data[0]
  end

  def size
    @data.length
  end

  def data
    @data.clone
  end

  def empty?
    @data.empty?
  end

  private

  def parent(idx)
    (idx - 1) / 2
  end

  def left(idx)
    2 * idx + 1
  end

  def right(idx)
    2 * idx + 2
  end

  def percolate_up!(idx)
    until idx.zero?
      pi = parent(idx)
      return unless @comparator.call(@data[idx], @data[pi]).positive?

      @data[pi], @data[idx] = @data[idx], @data[pi]
      idx = pi
    end
    nil
  end

  def percolate_down!(idx)
    l_idx = left(idx)
    r_idx = right(idx)
    value = @data[idx]

    while l_idx < @data.length
      nodes = { idx => @data[idx], l_idx => @data[l_idx] }
      nodes[r_idx] = @data[r_idx] unless @data[r_idx].nil?
      max_idx = nodes.keys.max { |i, j| @comparator.call(@data[i], @data[j]) }
      max_value = @data[max_idx]

      return if max_value == value

      @data[idx], @data[max_idx] = @data[max_idx], @data[idx]
      idx = max_idx
      l_idx = left(idx)
      r_idx = right(idx)
    end
    nil
  end

  def largest_internal_node
    @data.length / 2 - 1
  end

  def heapify!
    idx = largest_internal_node
    until idx.negative?
      percolate_down!(idx)
      idx -= 1
    end
    nil
  end
end
