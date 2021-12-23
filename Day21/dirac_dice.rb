class DiracDice
  DICE_NUMBERS = [1, 2, 3].freeze
  ROLL_NUMBERS = DICE_NUMBERS.product(*([DICE_NUMBERS] * 5)).freeze
  ROLL_SUMS = {}
  ROLL_NUMBERS.each do |roll|
    sums = [roll[0...3].sum, roll[3..].sum]
    ROLL_SUMS[sums] = ROLL_SUMS.fetch(sums, 0) + 1
  end
  ROLL_SUMS.freeze
end
