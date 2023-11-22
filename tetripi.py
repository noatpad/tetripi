import time
from tetris import Tetris
from inout import left_button

FPS = 1/30

def tetripi():
  print('Hello tetripi')
  tetris = Tetris()

  running = True
  while running:
    tetris.update()
    tetris.draw()
    # time.sleep(FPS)

    # print(f'{button_l.value}, {button_l.is_active}, {button_l.is_held}')


if __name__ == '__main__':
  tetripi()
