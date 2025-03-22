# library: https://github.com/sparkfun/qwiic_rv-8803_py
# tested with:
# SparkFun Real Time Clock Sensor - RV8803
#  - https://www.sparkfun.com/products/16281

# mpremote mip install github:sparkfun/qwiic_rv-8803_py

# Example based on https://github.com/sparkfun/qwiic_rv-8803_py/blob/master/README.md

import qwiic_i2c     # mpremote mip install github:sparkfun/qwiic_i2c_py
import qwiic_rv8803  # mpremote mip install github:sparkfun/qwiic_rv-8803_py
import sys
import time

I2C_SDA_PIN = 6
I2C_SCL_PIN = 7
RTC_I2C_Address = 0x32

i2c_bus = qwiic_i2c.get_i2c_driver(sda=I2C_SDA_PIN, scl=I2C_SCL_PIN, freq=100000)

def runExample():
  print("\nQwiic RV8803 Example Get Time\n")

  myRTC = qwiic_rv8803.QwiicRV8803(address=RTC_I2C_Address, i2c_driver=i2c_bus)

  if myRTC.is_connected() == False:
    print("The device isn't connected to the system. Please check your connection", \
      file=sys.stderr)
    return

  myRTC.begin()

# Uncomment the block below if you want to set the date and time
#   sec = 0
#   minute = 55
#   hour = 17
#   date = 22
#   month = 3
#   weekday = myRTC.kSaturday
#   year = 2025
#   myRTC.set_time(sec, minute, hour, weekday, date, month, year)

# Set time format for the current instance
  myRTC.set_24_hour()

  while True:
    myRTC.update_time()
    print ("Current Time: ", end="")
    print (myRTC.string_date(), end="")
    print (" ", myRTC.string_time())
    time.sleep(1)

if __name__ == '__main__':
  try:
    runExample()
  except (KeyboardInterrupt, SystemExit) as exErr:
    print("\nEnding Example")
    sys.exit(0)
