import numpy as np

class Cuboid:
  AXES = np.array([0, 1, 2])

  def __init__(self, cuboid):
    (low_x, high_x), (low_y, high_y), (low_z, high_z) = cuboid
    self.low_x = low_x
    self.high_x = high_x
    self.low_y = low_y
    self.high_y = high_y
    self.low_z = low_z
    self.high_z = high_z

  def width(self):
    return self.high_x - self.low_x + 1

  def height(self):
    return self.high_y - self.low_y + 1

  def depth(self):
    return self.high_z - self.low_z + 1

  def dimensions(self):
    return (self.width(), self.height(), self.depth())

  def cubes(self):
    return self.width() * self.height() * self.depth()

  def is_completely_outside_of(self, other_cuboid):
    return self.low_x > other_cuboid.high_x or self.high_x < other_cuboid.low_x or \
      self.low_y > other_cuboid.high_y or self.high_y < other_cuboid.low_y or \
      self.low_z > other_cuboid.high_z or self.high_z < other_cuboid.low_z

  def collides_with(self, other_cuboid):
    return not self.is_completely_outside_of(other_cuboid)

  def __str__(self):
    return self.as_tuple().__str__()

  def __repr__(self):
    return self.as_tuple().__repr__()

  def __sub__(self, other):
    '''Returns the cuboid which is the set of cubes of self that don't intersect with other'''
    axes = np.array([0, 1, 2])
    lower_inside = np.array([ (self.bounds(axis)[0] >= other.bounds(axis)[0] and \
                                self.bounds(axis)[0] <= other.bounds(axis)[1]) for axis in range(3) ])
    higher_inside = np.array([ (self.bounds(axis)[1] >= other.bounds(axis)[0] and \
                                self.bounds(axis)[1] <= other.bounds(axis)[1]) for axis in range(3) ])
    completely_inside = lower_inside & higher_inside

    contained_axes = completely_inside.sum()
    if self.is_completely_outside_of(other):
      return set([self])
    if contained_axes == 3: # if self is completely_inside other
      return set() # No cubes don't intersect
    if contained_axes == 2:
      # one axis sticks out
      outer_index = axes[~completely_inside][0] # get the axis which is sticking out
      if lower_inside[outer_index] or higher_inside[outer_index]:
        return self.__handle_case_where_one_face_sticks_out(other, outer_index)
      else:
        return self.__handle_case_where_two_faces_stick_out_in_one_axis(other, outer_index)
    if contained_axes == 1:
      # two axes stick out
      # axes that completely stick out
      outside_axes = ~lower_inside & ~higher_inside
      axes_completely_containing_self = outside_axes.sum()
      if axes_completely_containing_self == 0:
        return self.__handle_case_where_two_faces_stick_out_in_different_axes(other)
      elif axes_completely_containing_self == 1:
        return self.__handle_case_where_three_faces_stick_out_in_two_axes(other)
      elif axes_completely_containing_self == 2:
        return self.__handle_case_where_four_faces_stick_out_in_two_axes(other)
    if contained_axes == 0:
      # all axes stick out
      inner_axes = (lower_inside | higher_inside).sum()
      if inner_axes == 3:
        return self.__handle_case_where_three_faces_stick_out_in_three_axes(other)
      elif inner_axes == 2:
        return self.__handle_case_where_four_faces_stick_out_in_three_axes(other)
      elif inner_axes == 1:
        return self.__handle_case_where_five_faces_stick_out(other)
      else:
        return self.__handle_case_where_self_contains(other)
    return set()

  def bounds(self, axis = None):
    bounds = np.array(self.as_tuple())
    if axis is not None:
      # print(bounds[axis])
      pass
    return bounds if axis is None else bounds[axis]

  def midpoint(self, axis):
    low, high = self.bounds(axis)
    mid = (low + high) // 2
    return mid

  def as_tuple(self):
    return ((self.low_x, self.high_x), (self.low_y, self.high_y), (self.low_z, self.high_z))

  def __hash__(self):
    return self.as_tuple().__hash__()

  def __eq__(self, other):
    return self.__hash__() == other.__hash__()

  def combine_to_cuboids(self, other_cuboids):
    '''Returns a set of cuboids which represent the union of self and other_cuboids'''
    cuboids = set([self]) # working set of cuboids representing self - other_cuboids
    processed = set() # which of other_cuboids we've already processed
    for other in other_cuboids:
      exclusive = set() # keep a temporary set of cuboids that we've iterated through
      while len(cuboids) > 0:
        cuboid = cuboids.pop()
        if cuboid.collides_with(other):
          exclusive.discard(cuboid)
          cuboid_exclusive = (cuboid - other)
          cuboids |= cuboid_exclusive
        else:
          exclusive.add(cuboid)
      cuboids = exclusive
      processed.add(other)
    other_cuboids |= cuboids
    other_cuboids |= processed
    return cuboids

  def remove_colliding_cuboids(self, other_cuboids):
    '''Updates the set of other_cuboids to be the set representing other_cuboids - self'''
    processed = set()
    while len(other_cuboids) > 0:
      other_cuboid = other_cuboids.pop()
      if self.collides_with(other_cuboid):
        processed |= (other_cuboid - self)
      else:
        processed.add(other_cuboid)
    other_cuboids |= processed
    return other_cuboids

  def __cut_along_axis(self, axis, cut_position, flush_lower = True):
    '''Returns this split along the given axis at the cut_position'''
    lower_bounds = self.bounds()
    higher_bounds = self.bounds()
    low, high = self.bounds(axis)
    if not low <= cut_position <= high:
      return None, None
    if not flush_lower:
      cut_position -= 1
    lower_bounds[axis] = (low, cut_position)
    higher_bounds[axis] = (cut_position + 1, high)
    lower = Cuboid(lower_bounds)
    higher = Cuboid(higher_bounds)
    bit, remaining = (higher, lower) if flush_lower else (lower, higher)
    return bit, remaining

  def __handle_case_where_one_face_sticks_out(self, other, outer_index):
    '''When only one face sticks out'''
    lower_inside = np.array([ (self.bounds(axis)[0] >= other.bounds(axis)[0] and \
                                self.bounds(axis)[0] <= other.bounds(axis)[1]) for axis in range(3) ])
    higher_inside = np.array([ (self.bounds(axis)[1] >= other.bounds(axis)[0] and \
                                self.bounds(axis)[1] <= other.bounds(axis)[1]) for axis in range(3) ])
    outside = set()
    low, high = self.bounds(outer_index)
    cut_position = other.bounds(outer_index)[(1 if lower_inside[outer_index] else 0)]
    bit, _ = self.__cut_along_axis(outer_index, cut_position, flush_lower = lower_inside[outer_index])
    outside.add(bit)
    return outside

  def __handle_case_where_two_faces_stick_out_in_one_axis(self, other, outer_index):
    '''Where two faces stick out but along the same axis'''
    lower_inside = np.array([ (self.bounds(axis)[0] >= other.bounds(axis)[0] and \
                                self.bounds(axis)[0] <= other.bounds(axis)[1]) for axis in range(3) ])
    higher_inside = np.array([ (self.bounds(axis)[1] >= other.bounds(axis)[0] and \
                                self.bounds(axis)[1] <= other.bounds(axis)[1]) for axis in range(3) ])
    completely_inside = lower_inside & higher_inside
    # split the cuboid and recursively subtract the pieces
    outside = set()
    left_bounds = self.bounds()
    right_bounds = self.bounds()
    low, high = other.bounds(outer_index)
    left_bounds[outer_index] = (self.bounds(outer_index)[0], low - 1)
    right_bounds[outer_index] = (high + 1, self.bounds(outer_index)[1])
    left = Cuboid(left_bounds)
    right = Cuboid(right_bounds)
    outside.add(left)
    outside.add(right)
    return outside

  def __handle_case_where_two_faces_stick_out_in_different_axes(self, other):
    '''When two faces stick out along different axes'''
    lower_inside = np.array([ (self.bounds(axis)[0] >= other.bounds(axis)[0] and \
                                self.bounds(axis)[0] <= other.bounds(axis)[1]) for axis in range(3) ])
    higher_inside = np.array([ (self.bounds(axis)[1] >= other.bounds(axis)[0] and \
                                self.bounds(axis)[1] <= other.bounds(axis)[1]) for axis in range(3) ])
    completely_inside = lower_inside & higher_inside

    outside = set()
    outside_axes = ~lower_inside | ~higher_inside
    primary_axis, secondary_axis = Cuboid.AXES[outside_axes]
    primary_bounds = self.bounds()
    secondary_bounds = self.bounds()
    # split cuboid along primary axis
    low, high = other.bounds(primary_axis)
    cut_position = (high if lower_inside[primary_axis] else low)
    primary, remaining = self.__cut_along_axis(primary_axis, cut_position, flush_lower = lower_inside[primary_axis])

    outside.add(primary)
    # recursively split remaining along secondary_axis
    outside |= (remaining - other)

    return outside

  def __handle_case_where_three_faces_stick_out_in_two_axes(self, other):
    '''When three faces stick out among two axes'''
    lower_inside = np.array([ (self.bounds(axis)[0] >= other.bounds(axis)[0] and \
                                self.bounds(axis)[0] <= other.bounds(axis)[1]) for axis in range(3) ])
    higher_inside = np.array([ (self.bounds(axis)[1] >= other.bounds(axis)[0] and \
                                self.bounds(axis)[1] <= other.bounds(axis)[1]) for axis in range(3) ])
    outside = set()

    secondary_axis = Cuboid.AXES[~lower_inside ^ ~higher_inside][0]
    # split cuboid along secondary axis
    low, high, = other.bounds(secondary_axis)
    cut_position = (high if lower_inside[secondary_axis] else low)
    main, remaining = self.__cut_along_axis(secondary_axis, cut_position, flush_lower = lower_inside[secondary_axis])
    outside.add(main)
    outside |= (remaining - other)

    return outside

  def __handle_case_where_three_faces_stick_out_in_three_axes(self, other):
    lower_inside = np.array([ (self.bounds(axis)[0] >= other.bounds(axis)[0] and \
                                self.bounds(axis)[0] <= other.bounds(axis)[1]) for axis in range(3) ])
    higher_inside = np.array([ (self.bounds(axis)[1] >= other.bounds(axis)[0] and \
                                self.bounds(axis)[1] <= other.bounds(axis)[1]) for axis in range(3) ])
    outside = set()

    # split cuboid along x
    low, high = other.bounds(0)
    cut_position = (high if lower_inside[0] else low)
    x_bit, remaining = self.__cut_along_axis(0, cut_position, flush_lower = lower_inside[0])
    outside.add(x_bit)
    outside |= (remaining - other)

    return outside

  def __handle_case_where_four_faces_stick_out_in_three_axes(self, other):
    lower_inside = np.array([ (self.bounds(axis)[0] >= other.bounds(axis)[0] and \
                                self.bounds(axis)[0] <= other.bounds(axis)[1]) for axis in range(3) ])
    higher_inside = np.array([ (self.bounds(axis)[1] >= other.bounds(axis)[0] and \
                                self.bounds(axis)[1] <= other.bounds(axis)[1]) for axis in range(3) ])
    outside = set()

    # split cuboid along one of the secondary axes
    secondary_axis = Cuboid.AXES[~lower_inside ^ ~higher_inside][0]
    low, high, = other.bounds(secondary_axis)
    cut_position = (high if lower_inside[secondary_axis] else low)
    main, remaining = self.__cut_along_axis(secondary_axis, cut_position, flush_lower = lower_inside[secondary_axis])
    outside.add(main)
    outside |= (remaining - other)

    return outside

  def __handle_case_where_four_faces_stick_out_in_two_axes(self, other):
    lower_inside = np.array([ (self.bounds(axis)[0] >= other.bounds(axis)[0] and \
                                self.bounds(axis)[0] <= other.bounds(axis)[1]) for axis in range(3) ])
    higher_inside = np.array([ (self.bounds(axis)[1] >= other.bounds(axis)[0] and \
                                self.bounds(axis)[1] <= other.bounds(axis)[1]) for axis in range(3) ])
    outside = set()

    # split cuboid along one of the secondary axes
    secondary_axis = Cuboid.AXES[~lower_inside & ~higher_inside][0]
    cut_position = other.midpoint(secondary_axis)
    bit, remaining = self.__cut_along_axis(secondary_axis, cut_position)
    outside |= (bit - other)
    outside |= (remaining - other)

    return outside

  def __handle_case_where_five_faces_stick_out(self, other):
    lower_inside = np.array([ (self.bounds(axis)[0] >= other.bounds(axis)[0] and \
                                self.bounds(axis)[0] <= other.bounds(axis)[1]) for axis in range(3) ])
    higher_inside = np.array([ (self.bounds(axis)[1] >= other.bounds(axis)[0] and \
                                self.bounds(axis)[1] <= other.bounds(axis)[1]) for axis in range(3) ])
    outside = set()

    # split cuboid along the main (short) axis
    main_axis = Cuboid.AXES[~lower_inside ^ ~higher_inside][0]
    low, high, = other.bounds(main_axis)
    cut_position = (high if lower_inside[main_axis] else low)
    bit, remaining = self.__cut_along_axis(main_axis, cut_position, flush_lower = lower_inside[main_axis])
    outside.add(bit)
    outside |= (remaining - other)

    return outside

  def __handle_case_where_self_contains(self, other):
    outside = set()

    # split cuboid along x axis
    x_axis = 0
    cut_position = other.midpoint(x_axis)
    left, right = self.__cut_along_axis(x_axis, cut_position)
    outside |= (left - other)
    outside |= (right - other)

    return outside


