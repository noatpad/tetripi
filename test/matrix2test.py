import board
from adafruit_ht16k33.matrix import MatrixBackpack16x8

i2c = board.I2C()
matrix = MatrixBackpack16x8(i2c)

matrix.brightness = 0.5
matrix.fill(0)
