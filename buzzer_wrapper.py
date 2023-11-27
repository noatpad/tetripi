from enum import Enum
from time import time, sleep
from threading import Thread
from gpiozero import TonalBuzzer
from buzzer_beep import Beep, Pause

beep_move = [Beep('E4')]

Sounds = Enum('Beeps', ['Move', 'Rotate', 'Fall', 'Hard_Drop', 'Invalid_Move',
                        'Land', 'Clear', 'Game'])
Sound_Map = {
  Sounds.Move: [Beep('C4')],
  Sounds.Rotate: [Beep('B3')],
  Sounds.Fall: [Beep('C4')],
  Sounds.Hard_Drop: [Beep('E4')],
  Sounds.Invalid_Move: [Beep('A3')],
  Sounds.Land: [Beep('D4')],
  Sounds.Clear: [Beep('A5', 0.05)],
  Sounds.Game: [Beep('B3', 0.4), Beep('A3', 0.4), Pause(0.8), Beep('B3', 0.4), Beep('A3', 0.4)]
}

class Buzzer_Wrapper:
  def __init__(self, pin: int):
    self.buzzer = TonalBuzzer(pin)
    self.thread = Thread()
    self.last_run = time()

  def play(self, sound: Sounds, wait=False):
    try:
      self.last_run = time()
      thread = Thread(target=self.play_beeps, args=(Sound_Map[sound], self.last_run))
      thread.start()
      if wait:
        thread.join()
    except KeyError:
      print('No sound found!!')

  def play_beeps(self, beeps: list[Beep], exec_time: float):
    if self.buzzer.is_active:
      self.buzzer.stop()

    for beep in beeps:
      self.buzzer.play(beep.tone)
      sleep(beep.duration)
      if self.last_run == exec_time:
        self.buzzer.stop()
      else:
        return
