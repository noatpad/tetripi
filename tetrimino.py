from random import randrange
from inout import matrix

all_tetriminos =  [
  # I block
  [[4, 5, 6, 7], [1, 5, 9, 13]],
  # O block
  [[0, 1, 4, 5]],
  # T block
  [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],
  # J block
  [[0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10], [1, 2, 5, 9]],
  # L block
  [[2, 4, 5, 6], [0, 1, 5, 9], [4, 5, 6, 8], [1, 5, 9, 10]],
  # S block
  [[1, 2, 4, 5], [0, 4, 5, 9]],
  # Z block
  [[0, 1, 5, 6], [2, 6, 5, 9]]
]

drop_timer_reset = 25
blink_timer_reset = 7

class Tetrimino:
  def __init__(self, game, block_type: int = None) -> None:
    block_index = block_type if block_type is not None else randrange(len(all_tetriminos))
    self.shapes = all_tetriminos[block_index]
    self.rotation = 0
    self.landed = False
    self.game = game
    # Shift block to the center when needed
    self.x = int(matrix.cols / 2) - int(self.get_width() / 2)
    self.y = -1 if block_index == 0 else 0
    # Timers
    self.drop_timer = drop_timer_reset
    self.blink_timer = blink_timer_reset
    self.blink_on = True

  def get_shape(self) -> list[int]:
    return self.shapes[self.rotation]

  def get_blocks(self) -> list[tuple[int, int]]:
    return [(self.x + (i % 4), self.y + int(i / 4)) for i in self.get_shape()]

  def get_width(self) -> int:
    xs = [x % 4 for x in self.get_shape()]
    return max(xs) - min(xs) + 1

  def is_valid_move(self) -> bool:
    return all((x >= 0 and x < len(self.game.board[0]) and
                y >= 0 and y < len(self.game.board) and
                not self.game.board[y][x]) for (x, y) in self.get_blocks())

  # Returns True if the block successfully moved
  def move(self, right=True) -> bool:
    orig_x = self.x
    self.x += 1 if right else -1

    if self.is_valid_move():
      return True

    self.x = orig_x
    return False

  # Returns True if the block successfully rotated
  # NOTE: Rotate doesn't allow blocks going above threshold (can't rotate I-block at the top)
  def rotate(self, clockwise=True) -> bool:
    orig_rot = self.rotation
    self.rotation = (self.rotation + (1 if clockwise else -1)) % len(self.shapes)

    if self.is_valid_move():
      return True

    can_shift = True
    shifted = False
    while can_shift and not self.is_valid_move():
      can_shift = self.move() or self.move(False)
      shifted = shifted or can_shift

    if shifted:
      return True

    self.rotation = orig_rot
    return False

  def soft_drop(self):
    orig_y = self.y
    self.y += 1
    self.drop_timer = drop_timer_reset

    if not self.is_valid_move():
      self.y = orig_y
      self.landed = True

  def hard_drop(self):
    while not self.landed:
      self.soft_drop()

  def fall(self):
    self.drop_timer -= 1
    if not self.drop_timer:
      self.soft_drop()

  def blink(self):
    self.blink_timer -= 1
    if not self.blink_timer:
      self.blink_on = not self.blink_on
      self.blink_timer = blink_timer_reset
