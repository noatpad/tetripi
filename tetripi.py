import time
from tetris import Tetris

FPS = 1/30

def tetripi():
  print('Hello tetripi')
  tetris = Tetris()

  running = True
  prev_time = time.time()
  curr_time = prev_time
  dt = 0
  while running:
    prev_time = curr_time
    curr_time = time.time()
    dt += curr_time - prev_time
    if dt < FPS:
      continue

    tetris.update()
    tetris.draw()
    dt = 0
    # time.sleep(FPS)


if __name__ == '__main__':
  tetripi()
