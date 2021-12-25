import unittest
from cuboid import Cuboid

class TestCuboid(unittest.TestCase):

  def test_cuboid_dimensions(self):
    self.cuboid = Cuboid(((-1, 1), (-2, 2), (-3, 3)))
    self.assertEqual(self.cuboid.dimensions(), (3, 5, 7))

  def test_cuboid_cubes(self):
    self.cuboid = Cuboid(((-1, 1), (-2, 2), (-3, 3)))
    self.assertEqual(self.cuboid.cubes(), 3 * 5 * 7)

  def test_cuboid_outside_other(self):
    self.cuboid = Cuboid(((-2, -1), (-2, -1), (-2, -1)))
    self.other = Cuboid(((1, 2), (1, 2), (1, 2)))
    self.assertTrue(self.cuboid.is_completely_outside_of(self.other))

  def test_cuboid_collides_with_other(self):
    self.cuboid = Cuboid(((-2, 2), (-2, 2), (-2, 2)))
    self.other = Cuboid(((1, 3), (1, 2), (1, 2)))
    self.assertTrue(self.cuboid.collides_with(self.other))

  def test_subtraction_when_cuboid_is_outside_other(self):
    # cuboids are far apart
    self.cuboid = Cuboid(((-2, -1), (-2, -1), (-2, -1)))
    self.other = Cuboid(((1, 2), (1, 2), (1, 2)))
    self.assertEqual(self.cuboid - self.other, set([self.cuboid]))

  def test_subtraction_when_other_contains_cuboid(self):
    # other contains cuboid
    self.cuboid = Cuboid(((-1, 1), (-1, 1), (-1, 1)))
    self.other = Cuboid(((-2, 2), (-2, 2), (-2, 2)))
    actual = self.cuboid - self.other
    self.assertEqual(actual, set())

  def test_subtraction_when_one_face_sticks_out(self):
    # one face of cuboid sticks out
    self.other = Cuboid(((-2, 2), (-2, 2), (-2, 2)))
    self.cuboid = Cuboid(((-1, 1), (0, 3), (-1, 1)))
    actual = self.cuboid - self.other
    expected = set([Cuboid(((-1, 1), (3, 3), (-1, 1)))])
    self.assertEqual(actual, expected)
    while len(actual) > 0:
      cuboid = actual.pop()
      self.assertTrue(cuboid.is_completely_outside_of(self.other))

  def test_subtraction_when_two_faces_stick_out_along_same_axis(self):
    # two faces of cuboid sticks out along same axis
    self.other = Cuboid(((-2, 2), (-2, 2), (-2, 2)))
    self.cuboid = Cuboid(((-1, 1), (-3, 3), (-1, 1)))
    actual = self.cuboid - self.other
    lower = Cuboid(((-1, 1), (-3, -3), (-1, 1)))
    higher = Cuboid(((-1, 1), (3, 3), (-1, 1)))
    expected = set([lower, higher])
    self.assertEqual(actual, expected)
    while len(actual) > 0:
      cuboid = actual.pop()
      self.assertTrue(cuboid.is_completely_outside_of(self.other))

  def test_subtraction_when_two_faces_stick_out_along_different_axes(self):
    # two faces of cuboid sticks out along different axes
    self.other = Cuboid(((-2, 2), (-2, 2), (-2, 2)))
    self.cuboid = Cuboid(((-3, 0), (-1, 1), (0, 3)))
    actual = self.cuboid - self.other
    self.assertTrue(len(actual) > 0)
    while len(actual) > 0:
      cuboid = actual.pop()
      self.assertTrue(cuboid.is_completely_outside_of(self.other))

  def test_subtraction_when_three_faces_stick_out_along_two_axes(self):
    # three faces of cuboid sticks out, two along the same axis, the third different
    self.other = Cuboid(((-2, 2), (-2, 2), (-2, 2)))
    self.cuboid = Cuboid(((-3, 3), (-1, 1), (0, 3)))
    actual = self.cuboid - self.other
    self.assertTrue(len(actual) > 0)
    while len(actual) > 0:
      cuboid = actual.pop()
      self.assertTrue(cuboid.is_completely_outside_of(self.other))

  def test_subtraction_when_three_faces_stick_out_along_three_axes(self):
    # three faces of cuboid sticks out along different axes
    self.other = Cuboid(((-2, 2), (-2, 2), (-2, 2)))
    self.cuboid = Cuboid(((-3, 0), (-3, 0), (0, 3)))
    actual = self.cuboid - self.other
    self.assertTrue(len(actual) > 0)
    while len(actual) > 0:
      cuboid = actual.pop()
      self.assertTrue(cuboid.is_completely_outside_of(self.other))

  def test_subtraction_when_four_faces_stick_out_along_two_axes(self):
    # four faces of cuboid sticks out along two axes
    self.other = Cuboid(((-2, 2), (-2, 2), (-2, 2)))
    self.cuboid = Cuboid(((-3, 3), (-1, 1), (3, 3)))
    actual = self.cuboid - self.other
    self.assertTrue(len(actual) > 0)
    while len(actual) > 0:
      cuboid = actual.pop()
      self.assertTrue(cuboid.is_completely_outside_of(self.other))

  def test_subtraction_when_four_faces_stick_out_along_three_axes(self):
    # four faces of cuboid sticks out along three axes
    self.other = Cuboid(((-2, 2), (-2, 2), (-2, 2)))
    self.cuboid = Cuboid(((-3, 3), (0, 3), (0, 3)))
    actual = self.cuboid - self.other
    self.assertTrue(len(actual) > 0)
    while len(actual) > 0:
      cuboid = actual.pop()
      self.assertTrue(cuboid.is_completely_outside_of(self.other))

  def test_subtraction_when_five_faces_stick_out(self):
    # five faces of cuboid sticks out
    self.other = Cuboid(((-2, 2), (-2, 2), (-2, 2)))
    self.cuboid = Cuboid(((-3, 3), (0, 3), (-3, 3)))
    actual = self.cuboid - self.other
    self.assertTrue(len(actual) > 0)
    while len(actual) > 0:
      cuboid = actual.pop()
      self.assertTrue(cuboid.is_completely_outside_of(self.other))

  def test_subtraction_when_cuboid_contains_other(self):
    # six faces of cuboid sticks out
    self.other = Cuboid(((-2, 2), (-2, 2), (-2, 2)))
    self.cuboid = Cuboid(((-3, 3), (-3, 3), (-3, 3)))
    actual = self.cuboid - self.other
    self.assertTrue(len(actual) > 0)
    while len(actual) > 0:
      cuboid = actual.pop()
      self.assertTrue(cuboid.is_completely_outside_of(self.other))

  def test_small_example(self):
    self.other = Cuboid(((10, 10), (10, 10), (10, 10)))
    self.cuboid = Cuboid(((9, 11), (9, 11), (9, 11)))
    actual = self.cuboid - self.other
    self.assertTrue(len(actual) > 0)
    while len(actual) > 0:
      cuboid = actual.pop()
      self.assertTrue(cuboid.is_completely_outside_of(self.other))

if __name__ == '__main__':
  unittest.main()
