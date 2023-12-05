from gpiozero.tones import Tone

class Beep:
  def __init__(self, note: str, duration=0.1):
    self.tone = Tone(note) if note else None
    self.duration = duration

class Pause(Beep):
  def __init__(self, duration=0.1):
    super().__init__(None, duration)
