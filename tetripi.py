from time import time
from constants import fps
from tetris import Tetris
from inout import power_led, power_switch

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
        power_led.on()
      tetris.update()
      tetris.draw()
    elif tetris:
        tetris.quit()
        tetris = None
        power_led.off()

    dt = 0

if __name__ == '__main__':
  tetripi()
