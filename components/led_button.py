from gpiozero import Button, LED

class LED_Button:
  def __init__(self, buttonPin: int, ledPin: int):
    self.button = Button(buttonPin, hold_time=0.6)
    self.led = LED(ledPin)
    self.pressed = False
    self.held = False
    self.ran_pressed = False

    self.button.when_activated = self._activate
    self.button.when_held = self._hold
    self.button.when_deactivated = self._release

  def _activate(self):
    self.pressed = True
    self.led.on()

  def _hold(self):
    self.held = True

  def _release(self):
    self.pressed = False
    self.held = False
    self.ran_pressed = False
    self.led.off()

  def pressed_or_held(self) -> bool:
    if self.pressed and not self.ran_pressed:
      self.ran_pressed = True
      return True
    # IDEA: Throttle the held action to x amount of time
    return self.held
