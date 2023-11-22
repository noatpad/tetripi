from inout import matrix, left_button, right_button, a_button, b_button
from tetrimino import Tetrimino

class Tetris:
  board: list[list[bool]]
  rows: int
  cols: int
  active_piece: Tetrimino
  next_piece: Tetrimino

  def __init__(self):
    self.rows = matrix.rows
    self.cols = matrix.cols
    self.board = [[False] * self.cols for _ in range(self.rows)]
    self.active_piece = Tetrimino(self)
    self.next_piece = Tetrimino(self)

  def update(self):
    # Move active block
    if (left_button.pressed_or_held()):
      self.active_piece.move(False)
    if (right_button.pressed_or_held()):
      self.active_piece.move(True)
    if (a_button.pressed_or_held()):
      self.active_piece.rotate(True)
    if (b_button.pressed_or_held()):
      self.active_piece.soft_drop()
      # self.active_piece.hard_drop()
      # self.active_piece.rotate(False)

    # Naturally drop active piece and land it if needed
    self.active_piece.fall()
    if self.active_piece.landed:
      blocks = self.land_piece()
      rows = sorted(set([y for (_, y) in blocks]))
      self.clear_lines(rows)

  def draw(self):
    # Prepare data to display
    grid = [row[:] for row in self.board]

    # Draw active block
    for (x, y) in self.active_piece.get_blocks():
      grid[y][x] = True

    # Display
    matrix.display(grid)

  # Returns the blocks that have landed
  def land_piece(self) -> list[tuple[int, int]]:
    blocks = self.active_piece.get_blocks()
    for (x, y) in blocks:
      self.board[y][x] = True
    self.active_piece = self.next_piece
    self.next_piece = Tetrimino(self)
    return blocks

  # Returns the number of lines cleared
  def clear_lines(self, rows) -> int:
    cleared = 0
    for row in rows:
      if (all(x for x in self.board[row])):
        del self.board[row]
        self.board.insert(0, [False] * self.cols)
        cleared += 1
    return cleared
