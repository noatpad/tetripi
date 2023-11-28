from gpiozero import DigitalInputDevice, LED
from matrix_wrapper import Matrix_Wrapper
from button_wrapper import Button_Wrapper
from buzzer_wrapper import Buzzer_Wrapper

matrix = Matrix_Wrapper()
left_button = Button_Wrapper(5)
right_button = Button_Wrapper(6)
a_button = Button_Wrapper(13)
b_button = Button_Wrapper(19)
buzzer = Buzzer_Wrapper(16)
power_switch = DigitalInputDevice(12, pull_up=True)
power_led = LED(26)
