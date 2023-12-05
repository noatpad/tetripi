from typing import Callable

default_blink_duration = 7

class Timer:
  def __init__(self, duration: int, callback: Callable, recurring=False):
    self.duration = duration
    self.now = duration
    self.callback = callback
    self.recurring = recurring

  def update(self):
    self.now -= 1
    if not self.now:
      self.callback()
      if self.recurring:
        self.reset()

  def reset(self):
    self.now = self.duration

class On_Off_Timer(Timer):
  def __init__(self, duration=default_blink_duration, start_value=True):
    super().__init__(duration, self.toggle_value, recurring=True)
    self.on = start_value

  def toggle_value(self):
    self.on = not self.on
