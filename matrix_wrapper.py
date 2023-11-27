from typing import Any
import board
from adafruit_ht16k33.matrix import MatrixBackpack16x8

class Matrix_Wrapper:
  def __init__(self) -> None:
    self.matrix = MatrixBackpack16x8(board.I2C())
    self.matrix.brightness = 0.5
    self.rows = self.matrix.columns
    self.cols = self.matrix.rows
    self.buffer = [[None] * self.cols for _ in range(self.rows)]

  def __getattr__(self, name: str) -> Any:
    return self.matrix.__getattr__(name)

  # This is needed because the default coordinate system is for a different orientation
  def _pixel(self, x: int, y: int, val: bool|None = None) -> bool|None:
    return self.matrix.pixel(y, self.cols - x - 1, val)

  def _set(self, x: int, y: int, val: bool):
    self.buffer[y][x] = val
    self._pixel(x, y, val)

  def get(self, x: int, y: int) -> bool:
    return self._pixel(x, y)

  def on(self, x: int, y: int):
    self._set(x, y, True)

  def off(self, x: int, y: int):
    self._set(x, y, False)

  def toggle(self, x: int, y: int):
    self._set(x, y, not self.get(x, y))

  def display(self, data: list[list[bool]]):
    assert len(data) == self.rows, 'Number of rows does not match!'
    assert len(data[0]) == self.cols, 'Number of cols does not match!'

    for y, row in enumerate(data):
      for x, val in enumerate(row):
        if (data[y][x] != self.buffer[y][x]):
          self._set(x, y, val)
