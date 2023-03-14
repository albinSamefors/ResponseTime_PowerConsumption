from machine import Pin, lightsleep, deepsleep

PIN_NUMBER = 0
CALLBACK_PIN = Pin(PIN_NUMBER, Pin.OUT, Pin.PULL_DOWN)

def callback():
    CALLBACK_PIN.on()
    CALLBACK_PIN.off()

def lightsleep_test(interval_in_ms):
    lightsleep(interval_in_ms)
    callback()

def deepsleep_test(interval_in_ms):
    deepsleep(interval_in_ms)
    callback()


