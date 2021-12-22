class Vector3D
  attr_reader :data

  def initialize(x, y, z)
    @data = [x, y, z]
    @index = { x: 0, y: 1, z: 2 }
  end

  %i[x y z].each_with_index do |x, i|
    define_method(x) do
      @data[i]
    end

    define_method("#{x}=".to_sym) do |value|
      @data[i] = value
    end
  end

  def self.zero
    Vector3D.new(0, 0, 0)
  end

  def -@
    Vector3D.new(-x, -y, -z)
  end

  def +(other)
    Vector3D.new(x + other.x, y + other.y, z + other.z)
  end

  def -(other)
    Vector3D.new(x - other.x, y - other.y, z - other.z)
  end

  def eql?(other)
    @data == other.to_a
  end

  def zero?
    @data.all?(&:zero?)
  end

  def hash
    @data.hash
  end

  def ==(other)
    @data == other.to_a
  end

  def to_s
    "[#{x},#{y},#{z}]"
  end

  def to_a
    @data.clone
  end
end
