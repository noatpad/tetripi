# tetripi
> a final project for my graduate Hardware System Design course. in a nutshell, it's a box that plays Tetris! Mostly!

![IMG_6420](https://github.com/noatpad/tetripi/assets/21282515/9fa472ec-f5cf-40dd-9777-4d14769498c5)

Tetripi is a little program that runs Tetris on a Raspberry Pi, encased in a little arcade box. It makes use of a [16x8 LED Matrix]([url](https://www.adafruit.com/product/2040)https://www.adafruit.com/product/2040) to display the board and some buttons to control the game. It also features a power switch on the side to "turn off" the game (in reality, it is placed in standby mode) and turn it back on. A piezo buzzer is also used to provide audio feedback to the player.

To run the game, simply run on the command line `python tetripi.py` (using Python 3.x) and play as far as you can!

The following components were used:
- [16x8 LED Matrix + Backpack](https://www.adafruit.com/product/2040) (GPIO pins 2 and 3 for I2C) - Displays the tetris board
- [6 LED Pushbuttons](https://www.adafruit.com/product/1439) - Moves, rotates, and drops the active piece on the board. Each button is wired to 2 GPIO pins, one for input and the other for its LED
  - Up button uses pins GPIO pin 16 for input and GPIO pin 19 for light
  - Left button uses pins 5 and 6
  - Right button uses pins 20 and 21
  - Down button uses pins 12 and 13
  - A button (the right, blue button) uses pins 17 and 18
  - B button (the left, blue button) uses pins 23 and 24
- [Slide switch](https://www.adafruit.com/product/805) (GPIO pin 27) - Powers on and off the game
- [Piezo buzzer](https://www.adafruit.com/product/160) (GPIO pin 22) - Provides audio feedback to the player
