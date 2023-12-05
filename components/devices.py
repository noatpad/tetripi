from gpiozero import DigitalInputDevice
from components.led_matrix import LED_Matrix
from components.led_button import LED_Button
from components.sound_buzzer import Sound_Buzzer

matrix = LED_Matrix()
up_button = LED_Button(16, 19)
left_button = LED_Button(5, 6)
right_button = LED_Button(20, 21)
down_button = LED_Button(12, 13)
a_button = LED_Button(17, 18)
b_button = LED_Button(23, 24)
buzzer = Sound_Buzzer(22)
power_switch = DigitalInputDevice(27, pull_up=True)
