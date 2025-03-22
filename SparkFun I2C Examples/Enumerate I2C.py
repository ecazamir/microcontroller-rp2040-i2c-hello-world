# Based on https://github.com/sparkfun/Qwiic_I2C_Py library and examples

# Import the package
import qwiic_i2c # mpremote mip install github:sparkfun/qwiic_i2c_py

# Create the i2c object using the pin numbers from SparkFun Thing Plus RP2040
# MicroPython and CircuitPython - Specify SDA and SCL pins, and frequency
# SparkFun Thing Plus RP2040 I2C/Qwiic pins

I2C_SDA_PIN = 6
I2C_SCL_PIN = 7


i2c_bus = qwiic_i2c.get_i2c_driver(sda=I2C_SDA_PIN, scl=I2C_SCL_PIN, freq=100000)

# Perform scan of I2C bus
device_addresses = i2c_bus.scan()
print("Bus scan:", device_addresses)

# Check if a device with the specified address is connected
print("Pinging devices:")
for device_address in device_addresses:
  ping_result = i2c_bus.ping(device_address)
  print("Device is connected at address", hex(device_address), ":", ping_result)