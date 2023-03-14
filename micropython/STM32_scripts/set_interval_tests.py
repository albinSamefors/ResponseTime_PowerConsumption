import machine
import time

def lightsleep_test(interval_in_ms):
    machine.lightsleep(interval_in_ms)

def deepsleep_test(interval_in_ms):
    machine.deepsleep(interval_in_ms)