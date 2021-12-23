require './player'
require './universe'
require './dirac_dice'
require 'pry'

class QuantumGame
  BOARD = (1..10).to_a.freeze
  DICE_SIDES = [1, 2, 3].freeze
  WIN_CONDITION = 21

  def initialize(player_starting_conditions)
    @player1 = Player.new(player_starting_conditions[0])
    @player2 = Player.new(player_starting_conditions[1])
  end

  def play
    starting_universe = Universe.new(@player1.position, @player2.position, 0, 0)
    @win_cache = {}
    count_wins_in_universe(starting_universe)
  end

  private

  def count_wins_in_universe(universe)
    if universe.moving_player_score >= WIN_CONDITION || universe.idle_player_score >= WIN_CONDITION
      win = (universe.moving_player_score >= WIN_CONDITION ? [1, 0] : [0, 1])
      @win_cache[universe] = win
      return win
    end

    wins = [0, 0]
    possible_rolls.each do |sum, repeats|
      main_position = next_move(universe.moving_player_position, sum)
      # switch player turn
      new_universe = Universe.new(universe.idle_player_position, main_position,
                                  universe.idle_player_score, universe.moving_player_score + main_position)
      idle_wins, main_wins = @win_cache[new_universe] || count_wins_in_universe(new_universe)
      # multiply the wins by the repeats of the sum
      wins[0] += main_wins * repeats
      wins[1] += idle_wins * repeats
    end
    @win_cache[universe] = wins
  end

  def possible_rolls
    DiracDice::ROLL_SUMS
  end

  def next_move(position, sum)
    BOARD[(position + sum - 1) % BOARD.length]
  end
end
