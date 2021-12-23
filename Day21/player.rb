class Player
  INPUT_PATTERN = /(Player \d) starting position: (\d+)/.freeze

  attr_reader :id, :position, :score

  def initialize(input_string)
    @score = 0
    @id, @position = INPUT_PATTERN.match(input_string).captures.map(&:to_i)
  end

  def move_to(space)
    @position = space
    @score += space
  end
end
