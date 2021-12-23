class Universe
  attr_reader :player1_position, :player2_position, :player1_score, :player2_score

  def initialize(player1_position, player2_position, player1_score, player2_score)
    @player1_position = player1_position
    @player2_position = player2_position
    @player1_score = player1_score
    @player2_score = player2_score
  end

  def hash
    "#{player1_position},#{player2_position},#{player1_score},#{player2_score}".hash
  end

  def eql?(other)
    player1_score == other.player1_score \
      && player2_score == other.player2_score \
      && player1_position == other.player1_position \
      && player2_position == other.player2_position
  end
end
