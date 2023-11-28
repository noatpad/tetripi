from gpiozero import Button

class Button_Wrapper:
  def __init__(self, pin: int):
    self.button = Button(pin, hold_time=0.6)
    self.pressed = False
    self.held = False
    self.ran_pressed = False

    self.button.when_activated = self._activate
    self.button.when_held = self._hold
    self.button.when_deactivated = self._release

  def _activate(self):
    self.pressed = True

  def _hold(self):
    self.held = True

  def _release(self):
    self.pressed = False
    self.held = False
    self.ran_pressed = False

  def pressed_or_held(self) -> bool:
    if self.pressed and not self.ran_pressed:
      self.ran_pressed = True
      return True
    # IDEA: Throttle the held action to x amount of time
    return self.held
