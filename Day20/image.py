import numpy as np

class Image:
  LIGHT = '#'
  DARK = '.'
  SYMBOL_MAP = { DARK: '0', LIGHT: '1' }
  algorithm = ''

  def __init__(self, grid, algorithm = None):
    self._grid = np.array(grid)
    self._outside_symbol = Image.DARK
    if algorithm:
      Image.algorithm = algorithm

  def enhance(self):
    new_grid = self.__wrap(self._grid)
    it = np.nditer(new_grid, flags=['multi_index'])

    for x in it:
      r, c = it.multi_index
      considered_pixels = self.__centered_grid_at(r - 1, c - 1)
      binary_index = "".join([Image.SYMBOL_MAP[c] for c in considered_pixels.flat])
      new_grid[r, c] = self.__calculate_symbol_from_binary_index(binary_index)
    self.__enhance_outer_region()
    self._grid = new_grid

  def display(self):
    rows, cols = self._grid.shape
    output = "\n".join(map(lambda row: "".join(row), self.__wrap(self._grid).tolist()))
    print(output)

  def lit_pixel_count(self):
    return np.sum(self._grid == Image.LIGHT)

  def __wrap(self, grid):
    rows, cols = grid.shape
    rows += 2
    cols += 2
    wrapped_grid = [[grid[r - 1][c - 1] \
      if 0 < r < rows - 1 and 0 < c < cols - 1 else self._outside_symbol \
      for c in range(cols)] for r in range(rows)]
    return np.array(wrapped_grid)

  def __centered_grid_at(self, row, col):
    rows, cols = self._grid.shape
    considered_pixels = np.array([[self._grid[row + i, col + j] \
      if 0 <= row + i < rows and 0 <= col + j < cols \
      else self._outside_symbol \
      for j in range(-1, 2)] for i in range(-1, 2)])
    return considered_pixels

  def __enhance_outer_region(self):
    binary_index = Image.SYMBOL_MAP[self._outside_symbol] * 9
    self._outside_symbol = self.__calculate_symbol_from_binary_index(binary_index)

  def __calculate_symbol_from_binary_index(self, binary_index):
    index = int(binary_index, 2)
    return Image.algorithm[index]
