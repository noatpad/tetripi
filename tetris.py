from enum import Enum
from constants import blink_duration
from inout import matrix, left_button, right_button, a_button, b_button, buzzer
from tetrimino import Tetrimino
from buzzer_wrapper import Sounds
from tick_timer import Timer, On_Off_Timer

State = Enum('TetrisState', ['Holding', 'Dropping', 'GameOver'])

hold_duration = 25
min_speed = 48

class Tetris:
  def __init__(self):
    self.state = State.Holding
    self.rows = matrix.rows
    self.cols = matrix.cols
    self.board = [[False] * self.cols for _ in range(self.rows)]
    # Score and speed
    self.score = 0
    self.speed = min_speed
    # Pieces
    self.active_piece = Tetrimino(self)
    self.next_piece = Tetrimino(self)
    # Timers
    self.hold_timer = Timer(hold_duration, lambda: self.set_state(State.Dropping))
    self.game_over_blink_timer = On_Off_Timer(blink_duration)

  def set_state(self, state: State):
    self.state = state

  def update(self):
    if self.state == State.Holding:
      self.control_block(allow_drop=False)
      self.active_piece.blink()
      self.hold_timer.update()
    elif self.state == State.Dropping:
      self.control_block(True)
      self.active_piece.fall()
      if self.active_piece.landed:
        blocks = self.land_piece()
        rows = sorted(set([y for (_, y) in blocks]))
        self.clear_lines(rows)
        self.check_for_game_over()
    elif self.state == State.GameOver:
      self.game_over_blink_timer.update()

  def draw(self):
    # Prepare data to display
    grid = [row[:] for row in self.board]

    # Draw active block
    show_active_block = ((self.state == State.Holding and self.active_piece.blink_timer.on) or
                         (self.state == State.Dropping))
    if (show_active_block):
      for (x, y) in self.active_piece.get_blocks():
        grid[y][x] = True

    # Blink "game over" blocks if needed
    if (self.state == State.GameOver):
      for x in range(self.cols):
        grid[0][x] = self.game_over_blink_timer.on if grid[0][x] else False

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
    self.hold_timer.reset()
    self.set_state(State.Holding)
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

    lines = len(cleared)
    if lines:
      self.score += lines
      self.set_speed()

    return lines

  def check_for_game_over(self):
    if (any(x for x in self.board[0])):
      self.set_state(State.GameOver)
      buzzer.play(Sounds.Game)

  def set_speed(self):
    # For each 5 (originally 10) lines cleared, you go "up a level"
    lvl = int(self.score / 5) + 1
    if lvl <= 9:
      self.speed = min_speed - (lvl - 1) * 5
    elif lvl == 10:
      self.speed = 6
    elif lvl >= 11 and lvl <= 13:
      self.speed = 5
    elif lvl >= 14 and lvl <= 16:
      self.speed = 4
    elif lvl >= 17 and lvl <= 19:
      self.speed = 3
    elif lvl >= 20 and lvl <= 29:
      self.speed = 2
    else:
      self.speed = 1

    # Update timer durations on upcoming blocks
    # NOTE: Not exactly optimal
    self.active_piece.update_drop_duration(self.speed)
    self.next_piece.update_drop_duration(self.speed)

  def quit(self):
    matrix.clear()
