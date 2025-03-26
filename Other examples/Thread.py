# Example blinking led with a thread.

import time, _thread, machine

def task(n, delay):
    led = machine.Pin("LED", machine.Pin.OUT)
    for i in range(n):
        led.high()
        time.sleep(delay)
        led.low()
        time.sleep(delay)
    print('thread done')

_thread.start_new_thread(task, (10, 0.5))
print('thread started')
