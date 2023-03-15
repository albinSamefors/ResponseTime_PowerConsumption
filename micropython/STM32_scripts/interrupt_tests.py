from machine import Pin, lightsleep, deepsleep

PIN_NUMBER = 'A1'
CALLBACK_PIN = Pin(PIN_NUMBER, Pin.OUT, Pin.PULL_DOWN)

def callback():
    CALLBACK_PIN.on()
    CALLBACK_PIN.off()

def lightsleep_blinky_test():
    pass

def lightsleep_i2C_test():
    lightsleep()
    callback()

def deepsleep_i2C_test():
    deepsleep()
    callback()


