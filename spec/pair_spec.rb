require File.join(File.dirname(__FILE__), '..', 'Day18', 'pair')

RSpec.describe Pair do
  describe '#construct_from_string' do
    let(:pair) { described_class.construct_from_string(pair_string) }

    context 'when pair is a simple pair' do
      let(:pair_string) { '[1,2]' }

      it 'prints the correct to_s' do
        expect(pair.to_s).to eq(pair_string)
      end

      it 'assigns left element correctly' do
        expect(pair.left.to_s).to eq('1')
      end

      it 'assigns right element correctly' do
        expect(pair.right.to_s).to eq('2')
      end
    end

    context 'when pair is a nested pair' do
      let(:pair_string) { '[[1,9],[8,[5,6]]]' }

      it 'prints the correct to_s' do
        expect(pair.to_s).to eq(pair_string)
      end

      it 'assigns left element correctly' do
        expect(pair.left.to_s).to eq('[1,9]')
      end

      it 'assigns right element correctly' do
        expect(pair.right.to_s).to eq('[8,[5,6]]')
      end
    end
  end

  describe '#combine' do
    let(:result) { described_class.combine(x, y) }

    context 'when adding simple pairs' do
      let(:x) { described_class.construct_from_string('[1, 2]') }
      let(:y) { described_class.construct_from_string('[3, 4]') }

      it 'returns the correct result' do
        expect(result.to_s).to eq('[[1,2],[3,4]]')
      end
    end

    context 'when adding nested pairs' do
      let(:x) { described_class.construct_from_string('[[1,2],3]') }
      let(:y) { described_class.construct_from_string('[4,[[5,6],7]]') }

      it 'returns the correct result' do
        expect(result.to_s).to eq('[[[1,2],3],[4,[[5,6],7]]]')
      end
    end
  end

  describe '#explode!' do
    let(:pair) { described_class.construct_from_string(pair_string) }
    before { pair.explode! }

    context 'when exploding pair is left-most' do
      let(:pair_string) { '[[[[[9,8],1],2],3],4]' }

      it 'explodes correctly' do
        expect(pair.to_s).to eq('[[[[0,9],2],3],4]')
      end
    end

    context 'when exploding pair is right-most' do
      let(:pair_string) { '[7,[6,[5,[4,[3,2]]]]]' }

      it 'explodes correctly' do
        expect(pair.to_s).to eq('[7,[6,[5,[7,0]]]]')
      end
    end

    context 'when exploding pair is inside but to the right' do
      let(:pair_string) { '[[6,[5,[4,[3,2]]]],1]' }

      it 'explodes correctly' do
        expect(pair.to_s).to eq('[[6,[5,[7,0]]],3]')
      end
    end

    context 'when exploding pair is deep inside a balanced pair to the left' do
      let(:pair_string) { '[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]' }

      it 'explodes correctly' do
        expect(pair.to_s).to eq('[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]')
      end
    end

    context 'when exploding pair is deep inside a balanced pair to the right' do
      let(:pair_string) { '[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]' }

      it 'explodes correctly' do
        expect(pair.to_s).to eq('[[3,[2,[8,0]]],[9,[5,[7,0]]]]')
      end
    end
  end

  describe '#split' do
    context 'when using the class method' do
      it 'splits an even number correctly' do
        expect(described_class.split(10).to_s).to eq('[5,5]')
      end

      it 'splits an odd number correctly' do
        expect(described_class.split(11).to_s).to eq('[5,6]')
      end
    end

    context 'when called on a pair' do
      let(:pair) { described_class.construct_from_string(pair_string) }
      let(:result) { pair.split! }

      context 'when pair is a simple pair with a 11 on the left' do
        let(:pair_string) { '[11,1]' }

        it 'correctly splits the culprit' do
          pair.split!
          expect(pair.to_s).to eq('[[5,6],1]')
        end

        it 'returns true' do
          expect(result).to be(true)
        end
      end

      context 'when pair is a simple pair with a 11 on the right' do
        let(:pair_string) { '[1,11]' }

        it 'correctly splits the culprit' do
          pair.split!
          expect(pair.to_s).to eq('[1,[5,6]]')
        end

        it 'returns true' do
          expect(result).to be(true)
        end
      end

      context 'when pair is in a nested pair on the left' do
        let(:pair_string) { '[[2,[11,3]],1]' }

        it 'correctly splits the culprit' do
          pair.split!
          expect(pair.to_s).to eq('[[2,[[5,6],3]],1]')
        end

        it 'returns true' do
          expect(result).to be(true)
        end
      end

      context 'when pair is a complicated pair' do
        let(:pair_string) { '[[[[0,7],4],[15,[0,13]]],[1,1]]' }

        it 'correctly splits the culprit' do
          pair.split!
          expect(pair.to_s).to eq('[[[[0,7],4],[[7,8],[0,13]]],[1,1]]')
        end

        it 'returns true' do
          expect(result).to be(true)
        end
      end
    end
  end

  describe '#+' do
    let(:x) { described_class.construct_from_string('[[[[4,3],4],4],[7,[[8,4],9]]]') }
    let(:y) { described_class.construct_from_string('[1,1]') }

    it 'adds the example value correctly' do
      expect((x + y).to_s).to eq('[[[[0,7],4],[[7,8],[6,0]]],[8,1]]')
    end
  end

  describe '#abs' do
    let(:pair) { described_class.construct_from_string(pair_string) }

    context 'when given a simple pair' do
      let(:pair_string) { '[9,1]' }

      it 'calculates the magnitude correctly' do
        expect(pair.abs).to eq(29)
      end
    end

    context 'when given a nested pair' do
      let(:pair_string) { '[[9,1],[1,9]]' }

      it 'calculates the magnitude correctly' do
        expect(pair.abs).to eq(129)
      end
    end

    context 'when given a complicated pair' do
      let(:pair_string) { '[[1,2],[[3,4],5]]' }

      it 'calculates the magnitude correctly' do
        expect(pair.abs).to eq(143)
      end
    end
  end
end
