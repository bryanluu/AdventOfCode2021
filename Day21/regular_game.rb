require './player'
require './deterministic_dice'

class RegularGame
  BOARD = (1..10).to_a.freeze
  WIN_CONDITION = 1000

  attr_reader :winner, :loser, :dice

  def initialize(player_starting_conditions)
    @players = player_starting_conditions.map { |line| Player.new(line) }
    @dice = DeterministicDice.new
    @winner = nil
    @loser = nil
  end

  def play
    turn = 0
    loop do
      player = @players[turn]
      sum = @dice.roll_thrice
      new_position = BOARD[(player.position + sum - 1) % BOARD.length]
      player.move_to(new_position)
      turn = (turn + 1) % 2
      next if player.score < WIN_CONDITION

      @winner = player
      @loser = @players[turn]
      break
    end
    @loser.score * @dice.rolls
  end
end
