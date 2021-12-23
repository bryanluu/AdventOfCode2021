class DiracDice
  DICE_NUMBERS = [1, 2, 3].freeze
  ROLL_NUMBERS = DICE_NUMBERS.product(*([DICE_NUMBERS] * 2)).freeze
  ROLL_SUMS = {}
  ROLL_NUMBERS.each do |roll|
    sum = roll.sum
    ROLL_SUMS[sum] = ROLL_SUMS.fetch(sum, 0) + 1
  end
  ROLL_SUMS.freeze
end
