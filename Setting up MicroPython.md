# Why MicroPython

RP2040-based microcontrollers can run C++ code, or MicroPython.

Why one would want to use micropython? Maybe because certain devices have more up-to-date libraries written in python instead of C++?

## How to get it

The major change is in the python runtime, which has to be deployed onto the microcontroller.
One can download the .uf2 firmware file for SparkFun Thing Plus micropython firmware from here: <https://micropython.org/download/SPARKFUN_THINGPLUS/> .

As of today (2025.03.23), the latest Micropython for SparkFun Thing Plus RP2040 is v1.24.1 <https://micropython.org/resources/firmware/SPARKFUN_THINGPLUS-20241129-v1.24.1.uf2> <https://github.com/micropython/micropython/releases/tag/v1.24.1>

## How to upload it

As with any UF2 firmware for RP2040 boards: put the device in flash mode by pressing the 'Flash button', then copy the file over.

## What next?

You might want to:

- install `mpremote`, so that you can interact with the board, or to push libraries onto it
- install the Thonny IDE, so that you can develop in a friendlier environment
