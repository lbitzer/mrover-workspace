from math import ceil
import smbus
import time as t
import numpy as np

bus = smbus.SMBus(2)
# For adafruit accelerometer
I2C_ADDRESS = 0x53

# For multiplexer
I2C_MULT_ADDRESS = 0x70

I2C_REG = 0x04 #random number

def multi_read_write(channel): #0xC

    bus.write_byte_data(I2C_MULT_ADDRESS, I2C_REG, channel)

def enable():
    # sets justified bit to 0, 10-bit resolution, +- 16g, etc.
    bus.write_byte_data(I2C_ADDRESS, 0x31, 0x3)
    # Set everything in register 0x2E to 0
    # Prevents functions from generating interrupts
    bus.write_byte_data(I2C_ADDRESS, 0x2E, 0x0)
    # Set everything in register 0x1D to 10100
    # THRESH_TAP - Scale factor us 62.5 mg/LSB (0xFF = 16g)
    bus.write_byte_data(I2C_ADDRESS, 0x1D, 0x14)
    # irrelevant unless SINGLE TAP or DOUBLE TAP is enabled
    bus.write_byte_data(I2C_ADDRESS, 0x21, 0x32)
    # irrelevant unless SINGLE TAP or DOUBLE TAP is enabled
    bus.write_byte_data(I2C_ADDRESS, 0x22, 0x0)
    # irrelevant unless SINGLE TAP or DOUBLE TAP is enabled
    bus.write_byte_data(I2C_ADDRESS, 0x23, 0x0)
    # enables x y z axis for TAP detection, not super relevant
    bus.write_byte_data(I2C_ADDRESS, 0x2A, 0x7)
    # Important -  Set register to 100, Turns on measure,
    # turns off sleep, and turns of waking up during sleep.
    bus.write_byte_data(I2C_ADDRESS, 0x2D, 0x08)


def get_decimal(ls, ms):
    # Gets most significant bit (MSG) and shifts by 8
    high = read_data(ms) << 8

    # Combines MSB and LSB and scales based off of values in the
    # Arduino ADXL343 digital accelerometer library
    # multiplied by 9.8 again otherwise get output in terms of g
    return np.int16((high | read_data(ls))) * 0.004 * -9.80665 * 9.80665


# Gets raw byte data from address I2C_ADDRESS
def read_data(num):
    return bus.read_byte_data(I2C_ADDRESS, num)

# Data loop
def get_data():
    # time
    time = float_round(t.process_time(), 6, ceil)
    # Gets x y z data of the accelerometer and returns it
    x = float_round(get_decimal(0x32, 0x33), 6, ceil)
    y = float_round(get_decimal(0x34, 0x35), 6, ceil)
    z = float_round(get_decimal(0x36, 0x37), 6, ceil)
    output = str(time) + ',' + str(x) + ',' + str(y) + ',' + str(z) + '\n'
    return output

multi_read_write(0x1)
enable()
multi_read_write(0x2)
enable()
multi_read_write(0x4)
enable()
multi_read_write(0x8)
enable()
multi_read_write(0x10)
enable()
multi_read_write(0x20)
enable()

# channel 3 = 0x8
# channel 2 = 0x4

# Rounds the number to a number of decimal places
def float_round(num, places = 6, direction = ceil):
    return direction(num * (10**places)) / float(10**places)

data_file0 = open("output0.txt", "w")
data_file1 = open("output1.txt", "w")
data_file2 = open("output2.txt", "w")
data_file3 = open("output3.txt", "w")
data_file4 = open("output4.txt", "w")
data_file5 = open("output5.txt", "w")

while True:
    multi_read_write(0x1)
    data_file0.write(get_data())

    multi_read_write(0x2)
    data_file1.write(get_data())

    multi_read_write(0x4)
    data_file2.write(get_data())

    multi_read_write(0x8)
    data_file3.write(get_data())

    multi_read_write(0x10)
    data_file4.write(get_data())

    multi_read_write(0x20)
    data_file5.write(get_data())