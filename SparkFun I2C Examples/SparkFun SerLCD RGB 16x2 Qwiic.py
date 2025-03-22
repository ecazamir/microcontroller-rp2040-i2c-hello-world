#!/usr/bin/env python
#-----------------------------------------------------------------------------
# Example based on ex1_qwiic_serlcd_hello_world.py from https://github.com/sparkfun/qwiic_serlcd_py
# Simple example demonstrating how to print "hello world" and a counting number to the SerLCD (Qwiic).
#------------------------------------------------------------------------
#
# Written by Emil Cazamir, March 2025
# Tested with:
#  - SparkFun 16x2 SerLCD - RGB Backlight (Qwiic)
#    https://www.sparkfun.com/sparkfun-16x2-serlcd-rgb-backlight-qwiic.html
#  - SparkFun Thing Plus - RP2040
#    https://www.sparkfun.com/sparkfun-thing-plus-rp2040.html
#    Running MicroPython v1.24.1 https://micropython.org/download/SPARKFUN_THINGPLUS/

# How to use this:
# - Install Thonny IDE and mpremote on your machine
# - Ensure the device runs MicroPython
# - Install the libraries (you can use mpremote for that) on the device
# - Connect the board with the LCD module and with the development host PC
# - Create a new file and run it on the device

import qwiic_i2c     # mpremote mip install github:sparkfun/qwiic_i2c_py
import qwiic_serlcd  # mpremote mip install github:sparkfun/qwiic_serlcd_py
import time
import sys

# SparkFun Thing Plus RP2040 I2C/Qwiic pins
I2C_SDA_PIN = 6
I2C_SCL_PIN = 7

# SparkFun 16x2 RGB backlit i2c address https://www.sparkfun.com/sparkfun-16x2-serlcd-rgb-backlight-qwiic.html
SerLCD_I2C_Address = 0x72

def runExample():

  print("\nSparkFun Qwiic SerLCD   Example 1\n")
  myI2CBus = qwiic_i2c.get_i2c_driver(sda=I2C_SDA_PIN, scl=I2C_SCL_PIN, freq=100000)
  myLCD = qwiic_serlcd.QwiicSerlcd(SerLCD_I2C_Address, myI2CBus)
  if myLCD.is_connected == False:
    print("The Qwiic SerLCD device isn't connected to the system. Please check your connection", \
      file=sys.stderr)
    return

  myLCD.setBacklight(50, 200, 0) # Set backlight to a greenish color
  myLCD.setContrast(4) # set contrast. Lower to 0 for higher contrast.
  myLCD.clearScreen() # clear the screen - this moves the cursor to the home position as well

  time.sleep(1) # give a sec for system messages to complete
  # myLCD.setCursor(0,0) # This action is optional. The default cursor position is at char 0, on row 0
  myLCD.print("LCD example")
  # Move cursor at the beginning of the the 2nd row
  myLCD.setCursor(0,1)
  myLCD.print("Counter: ")
  counter = 0
  while True:
    print("Counter: %d" % counter)
    # Move the cursor on the LCD after "Counter"
    myLCD.setCursor(9,1)
    myLCD.print(str(counter))
    counter = counter + 1
    time.sleep(1)

if __name__ == '__main__':
  try:
    runExample()
  except (KeyboardInterrupt, SystemExit) as exErr:
    print("\nEnding Example 1")
    sys.exit(0)
