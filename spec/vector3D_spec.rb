require File.join(File.dirname(__FILE__), '..', 'Tools', 'vector3D')

RSpec.fdescribe Vector3D do
  describe '#initialize' do
    let(:vector) { described_class.new(*data) }

    context 'when called with valid parameters' do
      let(:data) { [1, 2, 3] }

      it 'has the correct data' do
        expect(vector.to_a).to eq(data)
      end

      it 'defines appropriate getters' do
        expect(vector.x).to eq(data[0])
        expect(vector.y).to eq(data[1])
        expect(vector.z).to eq(data[2])
      end

      it 'defines appropriate setters' do
        vector.x += 1
        vector.y += 2
        vector.z += 3
        expect(vector.x).to eq(data[0] + 1)
        expect(vector.y).to eq(data[1] + 2)
        expect(vector.z).to eq(data[2] + 3)
      end
    end
  end

  describe '#zero' do
    let(:vector) { described_class.zero }

    it 'has the correct data' do
      expect(vector.to_a.all?(&:zero?)).to be(true)
    end
  end

  describe '#+' do
    let(:u) { described_class.new(*u_data) }
    let(:v) { described_class.new(*v_data) }
    let(:u_data) { [rand(100), rand(100), rand(100)] }
    let(:v_data) { [rand(100), rand(100), rand(100)] }
    let(:result) { u + v }

    it 'adds correctly' do
      expect(result.x).to eq(u_data[0] + v_data[0])
      expect(result.y).to eq(u_data[1] + v_data[1])
      expect(result.z).to eq(u_data[2] + v_data[2])
    end
  end

  describe '#-' do
    let(:u) { described_class.new(*u_data) }
    let(:v) { described_class.new(*v_data) }
    let(:u_data) { [rand(100), rand(100), rand(100)] }
    let(:v_data) { [rand(100), rand(100), rand(100)] }
    let(:result) { u - v }

    it 'subtracts correctly' do
      expect(result.x).to eq(u_data[0] - v_data[0])
      expect(result.y).to eq(u_data[1] - v_data[1])
      expect(result.z).to eq(u_data[2] - v_data[2])
    end
  end

  describe '#-@' do
    let(:vector) { described_class.new(*data) }
    let(:data) { [rand(100), rand(100), rand(100)] }
    let(:result) { -vector }

    it 'has correct data' do
      expect(result.x).to eq(-data[0])
      expect(result.y).to eq(-data[1])
      expect(result.z).to eq(-data[2])
    end
  end

  describe 'equality' do
    let(:u) { described_class.new(*data) }
    let(:v) { described_class.new(*data) }
    let(:data) { [rand(100), rand(100), rand(100)] }

    it 'tests equality correctly using eql?' do
      expect(u.eql? v).to be(true)
    end

    it 'tests equality correctly using ==' do
      expect(u).to eq(v)
    end
  end
end
