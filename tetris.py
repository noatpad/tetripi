from enum import Enum
from time import sleep
from inout import matrix, left_button, right_button, a_button, b_button, buzzer
from tetrimino import Tetrimino
from buzzer_wrapper import Sounds

State = Enum('TetrisState', ['Holding', 'Dropping', 'GameOver'])

hold_timer_reset = 25
game_over_blink_timer_reset = 7

class Tetris:
  def __init__(self):
    self.state = State.Holding
    self.rows = matrix.rows
    self.cols = matrix.cols
    self.board = [[False] * self.cols for _ in range(self.rows)]
    self.active_piece = Tetrimino(self)
    self.next_piece = Tetrimino(self)
    self.hold_timer = hold_timer_reset
    self.game_over_blink_timer = game_over_blink_timer_reset
    self.game_over_blink_on = True

  def update(self):
    if self.state == State.Holding:
      self.control_block(allow_drop=False)
      self.active_piece.blink()
      self.hold_timer -= 1
      if not self.hold_timer:
        self.state = State.Dropping
    elif self.state == State.Dropping:
      self.control_block(True)
      self.active_piece.fall()
      if self.active_piece.landed:
        blocks = self.land_piece()
        rows = sorted(set([y for (_, y) in blocks]))
        self.clear_lines(rows)
        self.check_for_game_over()
    elif self.state == State.GameOver:
      self.blink_game_over()

  def draw(self):
    # Prepare data to display
    grid = [row[:] for row in self.board]

    # Draw active block
    show_active_block = ((self.state == State.Holding and self.active_piece.blink_on) or
                         (self.state == State.Dropping))
    if (show_active_block):
      for (x, y) in self.active_piece.get_blocks():
        grid[y][x] = True

    # Blink "game over" blocks if needed
    if (self.state == State.GameOver):
      for x in range(self.cols):
        grid[0][x] = self.game_over_blink_on if grid[0][x] else False

    # Display
    matrix.display(grid)

  def control_block(self, allow_drop=True):
    # Move active block
    if (left_button.pressed_or_held()):
      self.active_piece.move(False)
    if (right_button.pressed_or_held()):
      self.active_piece.move(True)
    if (a_button.pressed_or_held()):
      self.active_piece.rotate(True)
    if (allow_drop and b_button.pressed_or_held()):
      self.active_piece.soft_drop()
      # self.active_piece.hard_drop()
      # self.active_piece.rotate(False)

  # Returns the blocks that have landed
  def land_piece(self) -> list[tuple[int, int]]:
    blocks = self.active_piece.get_blocks()
    for (x, y) in blocks:
      self.board[y][x] = True
    self.active_piece = self.next_piece
    self.next_piece = Tetrimino(self)
    self.hold_timer = hold_timer_reset
    self.state = State.Holding
    buzzer.play(Sounds.Land)
    return blocks

  # Returns the number of lines cleared
  def clear_lines(self, rows: list[int]) -> int:
    cleared = list(filter(lambda row: all(row for row in self.board[row]), rows))
    cleared_r = cleared.copy()
    cleared_r.reverse()
    for row in cleared_r:
      for col in range(self.cols):
        matrix.off(col, row)
        buzzer.play(Sounds.Clear, wait=True)

    for row in cleared:
      del self.board[row]
      self.board.insert(0, [False] * self.cols)
    return len(cleared)

  def check_for_game_over(self):
    if (any(x for x in self.board[0])):
      self.state = State.GameOver
      buzzer.play(Sounds.Game)

  def blink_game_over(self):
    self.game_over_blink_timer -= 1
    if not self.game_over_blink_timer:
      self.game_over_blink_on = not self.game_over_blink_on
      self.game_over_blink_timer = game_over_blink_timer_reset
