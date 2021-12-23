class Universe
  attr_reader :moving_player_position, :idle_player_position, :moving_player_score, :idle_player_score

  def initialize(moving_player_position, idle_player_position, moving_player_score, idle_player_score)
    @moving_player_position = moving_player_position
    @idle_player_position = idle_player_position
    @moving_player_score = moving_player_score
    @idle_player_score = idle_player_score
  end

  def hash
    to_a.hash
  end

  def to_a
    [moving_player_position, idle_player_position, moving_player_score, idle_player_score]
  end

  def eql?(other)
    to_a.eql?(other.to_a)
  end
end
