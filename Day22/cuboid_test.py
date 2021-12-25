import unittest
from cuboid import Cuboid

class TestCuboid(unittest.TestCase):

  def test_cuboid_dimensions(self):
    cuboid = Cuboid(((-1, 1), (-2, 2), (-3, 3)))
    self.assertEqual(cuboid.dimensions(), (3, 5, 7))

  def test_cuboid_cubes(self):
    cuboid = Cuboid(((-1, 1), (-2, 2), (-3, 3)))
    self.assertEqual(cuboid.cubes(), 3 * 5 * 7)

  def test_cuboid_outside_other(self):
    cuboid = Cuboid(((-2, -1), (-2, -1), (-2, -1)))
    other = Cuboid(((1, 2), (1, 2), (1, 2)))
    self.assertTrue(cuboid.is_completely_outside_of(other))

  def test_cuboid_collides_with_other(self):
    cuboid = Cuboid(((-2, 2), (-2, 2), (-2, 2)))
    other = Cuboid(((1, 3), (1, 2), (1, 2)))
    self.assertTrue(cuboid.collides_with(other))

  def test_subtraction_when_cuboid_is_outside_other(self):
    # cuboids are far apart
    cuboid = Cuboid(((-2, -1), (-2, -1), (-2, -1)))
    other = Cuboid(((1, 2), (1, 2), (1, 2)))
    self.assertEqual(cuboid - other, set([cuboid]))

  def test_subtraction_when_other_contains_cuboid(self):
    # other contains cuboid
    cuboid = Cuboid(((-1, 1), (-1, 1), (-1, 1)))
    other = Cuboid(((-2, 2), (-2, 2), (-2, 2)))
    actual = cuboid - other
    self.assertEqual(actual, set())

  def test_subtraction_when_one_face_sticks_out(self):
    # one face of cuboid sticks out
    other = Cuboid(((-2, 2), (-2, 2), (-2, 2)))
    cuboid = Cuboid(((-1, 1), (0, 3), (-1, 1)))
    actual = cuboid - other
    expected = set([Cuboid(((-1, 1), (3, 3), (-1, 1)))])
    self.assertEqual(actual, expected)
    while len(actual) > 0:
      cuboid = actual.pop()
      self.assertTrue(cuboid.is_completely_outside_of(other))

  def test_subtraction_when_two_faces_stick_out_along_same_axis(self):
    # two faces of cuboid sticks out along same axis
    other = Cuboid(((-2, 2), (-2, 2), (-2, 2)))
    cuboid = Cuboid(((-1, 1), (-3, 3), (-1, 1)))
    actual = cuboid - other
    lower = Cuboid(((-1, 1), (-3, -3), (-1, 1)))
    higher = Cuboid(((-1, 1), (3, 3), (-1, 1)))
    expected = set([lower, higher])
    self.assertEqual(actual, expected)
    while len(actual) > 0:
      cuboid = actual.pop()
      self.assertTrue(cuboid.is_completely_outside_of(other))

  def test_subtraction_when_two_faces_stick_out_along_different_axes(self):
    # two faces of cuboid sticks out along different axes
    other = Cuboid(((-2, 2), (-2, 2), (-2, 2)))
    cuboid = Cuboid(((-3, 0), (-1, 1), (0, 3)))
    actual = cuboid - other
    bits = [Cuboid(((-3, -3), (-1, 1), (0, 3))),
            Cuboid(((-2, 0), (-1, 1), (3, 3)))]
    expected = set(bits)
    self.assertEqual(actual, expected)
    while len(actual) > 0:
      cuboid = actual.pop()
      self.assertTrue(cuboid.is_completely_outside_of(other))

  def test_subtraction_when_three_faces_stick_out_along_two_axes(self):
    # three faces of cuboid sticks out, two along the same axis, the third different
    other = Cuboid(((-2, 2), (-2, 2), (-2, 2)))
    cuboid = Cuboid(((-3, 3), (-1, 1), (0, 3)))
    actual = cuboid - other
    bits = [Cuboid(((-3, 3), (-1, 1), (3, 3))),
            Cuboid(((-3, -3), (-1, 1), (0, 2))),
            Cuboid(((3, 3), (-1, 1), (0, 2)))]
    expected = set(bits)
    self.assertEqual(actual, expected)
    while len(actual) > 0:
      cuboid = actual.pop()
      self.assertTrue(cuboid.is_completely_outside_of(other))

  def test_subtraction_when_three_faces_stick_out_along_three_axes(self):
    # three faces of cuboid sticks out along different axes
    other = Cuboid(((-2, 2), (-2, 2), (-2, 2)))
    cuboid = Cuboid(((-3, 0), (-3, 0), (0, 3)))
    actual = cuboid - other
    bits = [Cuboid(((-3, -3), (-3, 0), (0, 3))),
            Cuboid(((-2, 0), (-3, -3), (0, 3))),
            Cuboid(((-2, 0), (-2, 0), (3, 3)))]
    expected = set(bits)
    self.assertEqual(actual, expected)
    while len(actual) > 0:
      cuboid = actual.pop()
      self.assertTrue(cuboid.is_completely_outside_of(other))

  def test_subtraction_when_four_faces_stick_out_along_two_axes(self):
    # four faces of cuboid sticks out along two axes
    other = Cuboid(((-2, 2), (-2, 2), (-2, 2)))
    cuboid = Cuboid(((-3, 3), (-1, 1), (-3, 3)))
    actual = cuboid - other
    bits = [Cuboid(((-3, -3), (-1, 1), (-3, 3))),
            Cuboid(((-2, 0), (-1, 1), (3, 3))),
            Cuboid(((-2, 0), (-1, 1), (-3, -3))),
            Cuboid(((1, 2), (-1, 1), (3, 3))),
            Cuboid(((1, 2), (-1, 1), (-3, -3))),
            Cuboid(((3, 3), (-1, 1), (-3, 3)))]
    expected = set(bits)
    self.assertEqual(actual, expected)
    while len(actual) > 0:
      cuboid = actual.pop()
      self.assertTrue(cuboid.is_completely_outside_of(other))

  def test_subtraction_when_four_faces_stick_out_along_three_axes(self):
    # four faces of cuboid sticks out along three axes
    other = Cuboid(((-2, 2), (-2, 2), (-2, 2)))
    cuboid = Cuboid(((-3, 3), (0, 3), (0, 3)))
    actual = cuboid - other
    bits = [Cuboid(((-3, 3), (3, 3), (0, 3))),
            Cuboid(((-3, 3), (0, 2), (3, 3))),
            Cuboid(((-3, -3), (0, 2), (0, 2))),
            Cuboid(((3, 3), (0, 2), (0, 2)))]
    expected = set(bits)
    self.assertEqual(actual, expected)
    while len(actual) > 0:
      cuboid = actual.pop()
      self.assertTrue(cuboid.is_completely_outside_of(other))

  def test_subtraction_when_five_faces_stick_out(self):
    # five faces of cuboid sticks out
    other = Cuboid(((-2, 2), (-2, 2), (-2, 2)))
    cuboid = Cuboid(((-3, 3), (0, 3), (-3, 3)))
    actual = cuboid - other
    bits = [Cuboid(((-3, 3), (3, 3), (-3, 3))),
            Cuboid(((-3, -3), (0, 2), (-3, 3))),
            Cuboid(((-2, 0), (0, 2), (-3, -3))),
            Cuboid(((-2, 0), (0, 2), (3, 3))),
            Cuboid(((1, 2), (0, 2), (-3, -3))),
            Cuboid(((1, 2), (0, 2), (3, 3))),
            Cuboid(((3, 3), (0, 2), (-3, 3)))]
    expected = set(bits)
    self.assertEqual(actual, expected)
    while len(actual) > 0:
      cuboid = actual.pop()
      self.assertTrue(cuboid.is_completely_outside_of(other))

  def test_subtraction_when_cuboid_contains_other(self):
    # six faces of cuboid sticks out
    other = Cuboid(((-2, 2), (-2, 2), (-2, 2)))
    cuboid = Cuboid(((-3, 3), (-3, 3), (-3, 3)))
    actual = cuboid - other
    bits = [Cuboid(((-3, -3), (-3, 3), (-3, 3))),
            Cuboid(((-2, 0), (-3, -3), (-3, 3))),
            Cuboid(((-2, 0), (3, 3), (-3, 3))),
            Cuboid(((-2, 0), (-2, 0), (-3, -3))),
            Cuboid(((-2, 0), (-2, 0), (3, 3))),
            Cuboid(((-2, 0), (1, 2), (-3, -3))),
            Cuboid(((-2, 0), (1, 2), (3, 3))),
            Cuboid(((1, 2), (-3, -3), (-3, 3))),
            Cuboid(((1, 2), (3, 3), (-3, 3))),
            Cuboid(((1, 2), (-2, 0), (-3, -3))),
            Cuboid(((1, 2), (-2, 0), (3, 3))),
            Cuboid(((1, 2), (1, 2), (-3, -3))),
            Cuboid(((1, 2), (1, 2), (3, 3))),
            Cuboid(((3, 3), (-3, 3), (-3, 3)))]
    expected = set(bits)
    self.assertEqual(actual, expected)
    while len(actual) > 0:
      cuboid = actual.pop()
      self.assertTrue(cuboid.is_completely_outside_of(other))

  def test_combine_to_cuboids(self):
    other_cuboid = Cuboid(((10, 12), (10, 12), (10, 12)))
    other_cuboids = set([other_cuboid])
    cuboid = Cuboid(((11, 13), (11, 13), (11, 13)))
    actual = cuboid.combine_to_cuboids(other_cuboids)
    expected = cuboid - other_cuboid
    self.assertEqual(actual, expected)
    self.assertEqual(other_cuboids, set([other_cuboid]) | expected)

  def test_remove_colliding_cuboids(self):
    other_cuboid = Cuboid(((10, 12), (10, 12), (10, 12)))
    other_cuboids = set([other_cuboid])
    cuboid = Cuboid(((11, 13), (11, 13), (11, 13)))
    actual = cuboid.remove_colliding_cuboids(other_cuboids)
    expected = other_cuboid - cuboid
    self.assertEqual(actual, expected)

if __name__ == '__main__':
  unittest.main()
