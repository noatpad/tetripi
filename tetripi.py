from time import time
from constants import fps
from tetris import Tetris

def tetripi():
  print('Hello tetripi')
  tetris = Tetris()

  running = True
  prev_time = time()
  curr_time = prev_time
  dt = 0
  while running:
    prev_time = curr_time
    curr_time = time()
    dt += curr_time - prev_time
    if dt < fps:
      continue

    tetris.update()
    tetris.draw()
    dt = 0


if __name__ == '__main__':
  tetripi()
