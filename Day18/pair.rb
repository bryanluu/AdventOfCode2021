require 'pry'

class Pair
  class << self
    def construct_from_string(pair_string)
      return pair_string.to_i unless pair_string.start_with?('[')

      left_string, right_string = Pair.split_element_string(pair_string)
      pair = Pair.new
      pair.left = Pair.construct_from_string(left_string)
      pair.right = Pair.construct_from_string(right_string)
      pair
    end

    def split_element_string(pair_string)
      unwrapped_string = pair_string[1...-1]
      stack = []
      unwrapped_string.each_char.each_with_index do |c, i|
        if c == '['
          stack.push(c)
        elsif c == ']'
          stack.pop
        elsif stack.empty? && c == ','
          left_string = unwrapped_string[0...i]
          right_string = unwrapped_string[(i + 1)..]
          return left_string, right_string
        end
      end
    end

    def combine(x, y)
      result = Pair.new
      result.left = x.clone
      result.right = y.clone
      result
    end

    def split(regular_number)
      result = Pair.new
      result.left = regular_number / 2
      result.right = (regular_number / 2.0).ceil
      result
    end
  end

  attr_accessor :parent
  attr_reader :left, :right

  def initialize
    @left = nil
    @right = nil
    @parent = nil
  end

  def left=(left)
    left = left.to_i unless left.is_a?(Pair)
    @left = left
    @left.parent = self if @left.is_a?(Pair)
  end

  def right=(right)
    right = right.to_i unless right.is_a?(Pair)
    @right = right
    @right.parent = self if @right.is_a?(Pair)
  end

  def left_child?
    parent&.left == self
  end

  def right_child?
    parent&.right == self
  end

  def explode!(depth = 0)
    if depth == 4
      increment_predecessor(left)
      increment_successor(right)
      replace_with_value(0)
      return true
    end

    return false unless left.is_a?(Pair) || right.is_a?(Pair)

    (left.is_a?(Pair) && left.explode!(depth + 1)) || (right.is_a?(Pair) && right.explode!(depth + 1))
  end

  def split!
    split = false
    split = left.split! if left.is_a?(Pair)
    return split if split

    if left.is_a?(Numeric) && left >= 10
      self.left = Pair.split(left)
      return true
    end

    split = right.split! if right.is_a?(Pair)
    return split if split

    if right.is_a?(Numeric) && right >= 10
      self.right = Pair.split(right)
      return true
    end

    false
  end

  def to_s
    "[#{left},#{right}]"
  end

  def +(other)
    result = Pair.combine(self, other)
    result.reduce!
  end

  def abs
    l = left.is_a?(Pair) ? left.abs : left
    r = right.is_a?(Pair) ? right.abs : right
    3 * l + 2 * r
  end

  def reduce!
    reduce = true
    while reduce
      reduce = explode!
      reduce ||= split!
    end
    self
  end

  def clone
    copy = Pair.new
    copy.left = left.clone
    copy.right = right.clone
    copy
  end

  private

  def increment_predecessor(value)
    pred_parent = self
    until pred_parent.right_child?
      pred_parent = pred_parent.parent
      return if pred_parent.nil?
    end
    pred_parent = pred_parent.parent
    if pred_parent.left.is_a?(Pair)
      pred_parent = pred_parent.left
      pred_parent = pred_parent.right while pred_parent.right.is_a?(Pair)
      pred_parent.right += value
    else
      pred_parent.left += value
    end
  end

  def increment_successor(value)
    succ_parent = self
    until succ_parent.left_child?
      succ_parent = succ_parent.parent
      return if succ_parent.nil?
    end
    succ_parent = succ_parent.parent
    if succ_parent.right.is_a?(Pair)
      succ_parent = succ_parent.right
      succ_parent = succ_parent.left while succ_parent.left.is_a?(Pair)
      succ_parent.left += value
    else
      succ_parent.right += value
    end
  end

  def replace_with_value(value)
    if left_child?
      parent.left = value
    elsif right_child?
      parent.right = value
    end
  end
end
