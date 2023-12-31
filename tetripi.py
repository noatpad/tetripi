from time import time
from tetris import Tetris
from components.devices import power_switch

fps = 1/30

def tetripi():
  tetris: Tetris = None
  prev_time = time()
  curr_time = prev_time
  dt = 0
  on = power_switch.is_active

  while True:
    prev_time = curr_time
    curr_time = time()
    dt += curr_time - prev_time
    if dt < fps:
      continue

    on = power_switch.is_active

    if on:
      if not tetris:
        tetris = Tetris()
      tetris.update()
      tetris.draw()
    elif tetris:
        tetris.quit()
        tetris = None

    dt = 0

if __name__ == '__main__':
  tetripi()
