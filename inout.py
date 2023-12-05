from gpiozero import DigitalInputDevice, LED
from matrix_wrapper import Matrix_Wrapper
from button_wrapper import Button_Wrapper
from buzzer_wrapper import Buzzer_Wrapper

matrix = Matrix_Wrapper()
up_button = Button_Wrapper(16, 19)
left_button = Button_Wrapper(5, 6)
right_button = Button_Wrapper(20, 21)
down_button = Button_Wrapper(12, 13)
a_button = Button_Wrapper(17, 18)
b_button = Button_Wrapper(23, 24)
buzzer = Buzzer_Wrapper(22)
power_switch = DigitalInputDevice(27, pull_up=True)
