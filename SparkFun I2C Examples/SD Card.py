# based on https://github.com/micropython/micropython-lib/tree/master/micropython/drivers/storage/sdcard
# using the example shown here: https://github.com/orgs/micropython/discussions/12305

# micropython - ThingPlus RP2040
# very basic boot.py to mount the SD card - scruss, 2024-11

import os, machine
from sdcard import SDCard  # need to `mpremote mip install sdcard`

spi = machine.SPI(1)  # on gpio 12, 14 and 15, with /CS on 9
sd = SDCard(spi, machine.Pin(9))
vfs = os.VfsFat(sd)
os.mount(vfs, "/sd")
