class Octopus:
  octopii = []

  def __init__(self, pos, energy):
    self._pos = pos
    self._energy = int(energy)
    self._active = True

  @property
  def position(self):
    return self._pos

  @property
  def energy(self):
    return self._energy

  @classmethod
  def populate(cls, lines):
    for r, line in enumerate(lines):
      row = []
      for c, e in enumerate(line.strip()):
        octopus = Octopus((r, c), e)
        row.append(octopus)
      cls.octopii.append(row)

  @classmethod
  def connect(cls):
    for r, row in enumerate(cls.octopii):
      for c, octopus in enumerate(row):
        tl = None
        tm = None
        tr = None
        ml = None
        mr = None
        bl = None
        bm = None
        br = None
        if r > 0:
          tm = cls.octopii[r-1][c]
          if c > 0:
            tl = cls.octopii[r-1][c-1]
          if c < len(cls.octopii[r-1]) - 1:
            tr = cls.octopii[r-1][c+1]
        if c > 0:
          ml = cls.octopii[r][c-1]
        if c < len(cls.octopii[r]) - 1:
          mr = cls.octopii[r][c+1]
        if r < len(cls.octopii) - 1:
          bm = cls.octopii[r+1][c]
          if c > 0:
            bl = cls.octopii[r+1][c-1]
          if c < len(cls.octopii[r-1]) - 1:
            br = cls.octopii[r+1][c+1]
        candidates = [tl, tm, tr, ml, mr, bl, bm, br]
        octopus._neighbors = [octo for octo in candidates if octo is not None]

  def flash(self):
    flashes = 1
    self._active = False
    for octo in self._neighbors:
      octo._energy += 1
      if octo.energy > 9 and octo._active:
        flashes += octo.flash()
    return flashes

  @classmethod
  def step(cls):
    flashes = 0
    for row in cls.octopii:
      for octo in row:
        octo._energy += 1
        octo._active = True
    for row in cls.octopii:
      for octo in row:
        if octo.energy > 9 and octo._active:
          flashes += octo.flash()
    for row in cls.octopii:
      for octo in row:
        if not octo._active:
          octo._energy = 0
    return flashes

  @classmethod
  def are_synchronized(cls):
    for row in cls.octopii:
      for octo in row:
        if octo.energy != 0:
          return False
    return True


  def __repr__(self):
    return f"<position: {self.position}, energy: {self.energy}, neighbors: {([octo.position for octo in self._neighbors])}>"

  @classmethod
  def display(cls):
    output = ""
    for row in cls.octopii:
      output += "".join([str(octo.energy) for octo in row])
      output += "\n"
    print(output)
