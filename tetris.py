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
      self.active_piece.rotate(False)

    # Naturally drop active piece and land it if needed
    self.active_piece.fall()
    if self.active_piece.landed:
      for (x, y) in self.active_piece.get_blocks():
        self.board[y][x] = True
      self.active_piece = self.next_piece
      self.next_piece = Tetrimino(self)

  def draw(self):
    # Prepare data to display
    grid = [row[:] for row in self.board]

    # Draw active block
    for (x, y) in self.active_piece.get_blocks():
      grid[y][x] = True

    # Display
    matrix.display(grid)
