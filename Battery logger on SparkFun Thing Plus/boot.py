# Mount SD card under /sd
import os, machine  # RTC, SPI
import qwiic_i2c  # mpremote mip install github:sparkfun/qwiic_i2c_py
import qwiic_rv8803  # mpremote mip install github:sparkfun/qwiic_rv-8803_py
import qwiic_ads1015  # mpremote mip install github:sparkfun/qwiic_ads1015_py
from sdcard import SDCard  # need to `mpremote mip install sdcard`

SD_MOUNT_PATH = "/sd"
VOLTAGE_LOG_FILE = SD_MOUNT_PATH + "/voltage.log"
HW_CLOCK_SF_RV8803_ATTACHED = False
ADC_ADS1015_ATTACHED = False

# I2C bus details, platform-specific
I2C_SDA_PIN = 6
I2C_SCL_PIN = 7
I2C_FREQUENCY = 100000  # Should keep i2c frequency up to 400000, the embedded battery gauge may not support higher frequency
HW_CLOCK_SF_RV8803_I2C_Address = 0x32
ADC_ADS1015_I2C_Address = 0x48

# I2C Device Map
i2c_device_aliases = {
    HW_CLOCK_SF_RV8803_I2C_Address: "SparkFun RTC module RV-8803",
    0x36: "SparkFun Thing Plus RP2040 Embedded Battery Gauge",
    ADC_ADS1015_I2C_Address: "Qwiic 12 Bit ADC - 4 Channel (ADS1015)",
}

ads1015_gain_map = {
    0x0000: "+/- 6.144 V",
    0x0200: "+/- 4.096 V",
    0x0400: "+/- 2.048 V",
    0x0600: "+/- 1.024 V",
    0x0800: "+/- 0.512 V",
    0x0A00: "+/- 0.256 V",
    0x0E00: "+/- 0.256 V",  # ??? Duplicate of 0x0a00 ?
}

ads1015_sample_rate_map = {
    0x0000: "128 Hz",
    0x0020: "250 Hz",
    0x0040: "490 Hz",
    0x0060: "920 Hz",
    0x0080: "1600 Hz",
    0x00A0: "2400 Hz",
    0x00C0: "3300 Hz",
}

# Machine RTC
rtc = machine.RTC()

# Initialize I2C
i2c_bus = qwiic_i2c.get_i2c_driver(sda=I2C_SDA_PIN, scl=I2C_SCL_PIN, freq=I2C_FREQUENCY)
i2c_device_addresses = i2c_bus.scan()
print("I2C Bus: devices found")
try:
    for i2c_device_address in i2c_device_addresses:
        print(
            f"  0x{i2c_device_address:02x}: Assuming {i2c_device_aliases[i2c_device_address]}"
        )
except Exception as e:
    print("  I2C Scan: Unknown device", e)

# Look for SparkFun RV-8803 Real Time Clock module
if HW_CLOCK_SF_RV8803_I2C_Address in i2c_device_addresses:
    HW_CLOCK_SF_RV8803_ATTACHED = True

# Look for SparkFun RV-8803 module and display message
if HW_CLOCK_SF_RV8803_ATTACHED:
    print(
        f"I2C: Treating device at {hex(HW_CLOCK_SF_RV8803_I2C_Address)} as SparkFun RTC module RV-8803"
    )
    HW_RTC_RV_8803 = qwiic_rv8803.QwiicRV8803(
        address=HW_CLOCK_SF_RV8803_I2C_Address, i2c_driver=i2c_bus
    )
    HW_RTC_RV_8803.begin()
    HW_RTC_RV_8803.set_24_hour()
    HW_RTC_RV_8803.update_time()
    print("RTC Date and time: " + HW_RTC_RV_8803.string_time_8601())
    # Setting machine RTC using values from the hardware RTC module
    # https://docs.micropython.org/en/latest/library/machine.RTC.html
    # Parameter order: (year, month, day, weekday, hours, minutes, seconds, subseconds)
    rtc.datetime(
        (
            HW_RTC_RV_8803.get_year(),
            HW_RTC_RV_8803.get_month(),
            HW_RTC_RV_8803.get_date(),
            HW_RTC_RV_8803.get_weekday(),
            HW_RTC_RV_8803.get_hours(),
            HW_RTC_RV_8803.get_minutes(),
            HW_RTC_RV_8803.get_seconds(),
            HW_RTC_RV_8803.get_hundredths(),
        )
    )

else:
    print("I2C: Real Time Clock module not found, not using it")
    mdt = machine.RTC().datetime()
    print(
        f"Machine RTC: {mdt[0]:04d}-{mdt[1]:02d}-{mdt[2]:02d}T{mdt[4]:02d}:{mdt[5]:02d}:{mdt[6]:02d}"
    )

# Initialize ADS1015 ADC if found
if ADC_ADS1015_I2C_Address in i2c_device_addresses:
    ADC_ADS1015_ATTACHED = True

if ADC_ADS1015_ATTACHED:
    print(
        f"I2C: Treating device at {hex(ADC_ADS1015_I2C_Address)} as SparkFun Qwiic 12 Bit ADC - 4 Channel (ADS1015)"
    )
    ADC_MODULE = qwiic_ads1015.QwiicADS1015(
        address=ADC_ADS1015_I2C_Address, i2c_driver=i2c_bus
    )
    # Re-check connection
    if ADC_MODULE.is_connected():
        print("I2C connection to ADC module is successful")
        print("Setting/getting ADS1015 ADC Parameters")
        ADC_MODULE.begin()
        ADC_MODULE.use_conversion_ready(True)
        # Set sample rate to 128 Hz
        # 0 = 128Hz, 0x20 / kConfigRate250Hz = 250Hz, 0x80 = 1600Hz (default), etc
        ADC_MODULE.set_sample_rate(ADC_MODULE.kConfigRate250Hz)
        # Set full range gain to 2.048V
        # 0x0400 / kConfigPga2 = 2.048V (default), kConfigPga4 = 1V, kConfigPga16/0x0a00 = 0.256V
        ADC_MODULE.set_gain(ADC_MODULE.kConfigPga2)
        print(
            f"  gain: 0x{ADC_MODULE.get_gain():04x} ({ads1015_gain_map[ADC_MODULE.get_gain()]})"
        )
        print(f"  multiplier: {ADC_MODULE.get_multiplier()}")
        print(
            f"  sampling rate: 0x{ADC_MODULE.get_sample_rate():04x} ({ads1015_sample_rate_map[ADC_MODULE.get_sample_rate()]})"
        )
    else:
        print("I2C connection to ADC module failed")
else:
    print("I2C: ADC ADS 1015 module not found, not using it")

# Mount the SD card
try:
    print("Trying to mount the SD card...")
    spi1 = machine.SPI(1)
    # on SparkFun Thing Plus 2040 The embedded SD card is at SPI(1)
    # gpio 12(miso), 14(sck) and 15(mosi), with CS on pin 9
    sd = SDCard(spi1, machine.Pin(9))
    vfs = os.VfsFat(sd)
    os.mount(vfs, SD_MOUNT_PATH)
    print("SD card mounted under " + SD_MOUNT_PATH)

except Exception as e:
    print("An error occurred while mounting the SD card:", e)
