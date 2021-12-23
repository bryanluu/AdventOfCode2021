require './player'
require './universe'
require './dirac_dice'

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
    return @win_cache[universe] if @win_cache.key?(universe)

    wins = [0, 0]
    possible_rolls.each do |sums, repeats|
      p1_sum, p2_sum = sums
      p1 = next_move(universe.player1_position, p1_sum)
      p2 = next_move(universe.player2_position, p2_sum)
      new_universe = Universe.new(p1, p2, universe.player1_score + p1, universe.player2_score + p2)
      if new_universe.player1_score >= WIN_CONDITION || new_universe.player2_score >= WIN_CONDITION
        @win_cache[new_universe] = (new_universe.player1_score >= WIN_CONDITION ? [repeats, 0] : [0, repeats])
      end
      p1_wins, p2_wins = @win_cache[new_universe] || count_wins_in_universe(new_universe)
      wins[0] += p1_wins
      wins[1] += p2_wins
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
