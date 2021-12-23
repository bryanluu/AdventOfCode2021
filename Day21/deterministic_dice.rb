class DeterministicDice
  attr_reader :number, :rolls

  def initialize
    @number = 0
    @rolls = 0
  end

  def roll_thrice
    # roll the dice three times and add their numbers
    sum = roll_numbers.sum
    @number = dice_number(@number + 3)
    @rolls += 3
    sum
  end

  private

  def roll_numbers
    [dice_number(@number + 1), dice_number(@number + 2), dice_number(@number + 3)]
  end

  def dice_number(num)
    (num - 1) % 100 + 1
  end
end
