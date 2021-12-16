require File.join(File.dirname(__FILE__), '..', 'Tools', 'heap')

describe Heap do
  describe '#initialize' do
    context 'by default' do
      let(:heap) { Heap.new }

      it 'creates an empty heap' do
        expect(heap.size).to eq(0)
      end

      it 'has no root' do
        expect(heap.root).to be_nil
      end

      it 'has no data' do
        expect(heap.data).to be_empty
      end
    end

    context 'when given data' do
      let(:heap) { Heap.new([0, 1, 2]) }

      it 'creates a heap with the correct size' do
        expect(heap.size).to eq(3)
      end

      it 'has the correct root' do
        expect(heap.root).to eq(2)
      end

      it 'has correct heapified data' do
        expect(heap.data).to eq([2, 1, 0])
      end
    end

    context 'when given a block' do
      let(:heap) { Heap.new([2, 1, 0]) { |x, y| x > y } }

      it 'creates a heap with the correct size' do
        expect(heap.size).to eq(3)
      end

      it 'has the correct root' do
        expect(heap.root).to eq(0)
      end

      it 'has correct heapified data' do
        expect(heap.data).to eq([0, 1, 2])
      end
    end
  end

  describe '#insert!' do
    context 'when heap is empty' do
      let(:heap) { Heap.new }

      before do
        heap.insert!(1)
      end

      it 'adds a single element' do
        expect(heap.size).to eq(1)
      end

      it 'maintains heap property' do
        expect(heap.data).to eq([1])
      end

      it 'updates the root correctly' do
        expect(heap.root).to eq(1)
      end
    end

    context 'when heap has a single element' do
      let(:heap) { Heap.new([0]) }

      before do
        heap.insert!(1)
      end

      it 'adds another element' do
        expect(heap.size).to eq(2)
      end

      it 'maintains heap property' do
        expect(heap.data).to eq([1, 0])
      end

      it 'updates the root correctly' do
        expect(heap.root).to eq(1)
      end
    end

    context 'when applied multiple times' do
      let(:heap) { Heap.new([0, 1, 3]) }

      before do
        heap.insert!(2)
      end

      it 'adds another element' do
        expect(heap.size).to eq(4)
      end

      it 'maintains heap property' do
        expect(heap.data).to eq([3, 0, 1, 2])
      end

      it 'updates the root correctly' do
        expect(heap.root).to eq(3)
      end
    end
  end

  describe '#extract!' do
    context 'when heap is empty' do
      let(:heap) { Heap.new }

      it 'returns nil' do
        expect(heap.extract!).to be_nil
      end
    end

    context 'when heap is non-empty' do
      let(:heap) { Heap.new([0, 1, 2, 3]) }

      it 'returns nil' do
        expect(heap.extract!).to be_nil
      end

      it 'maintains heap property' do
        heap.extract!
        expect(heap.data).to eq([2, 1, 0])
      end

      it 'reduces size by 1' do
        heap.extract!
        expect(heap.size).to eq(3)
      end
    end
  end
end
