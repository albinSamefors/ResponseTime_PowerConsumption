import machine
import utime
TIMER_PIN_NUMBER = "A0"
GREEN_LED = machine.Pin("B0", machine.Pin.OUT)
TIMER_PIN = machine.Pin(TIMER_PIN_NUMBER, machine.Pin.OUT,machine.Pin.PULL_DOWN)
RESPONSE_PIN_NUMBER ='A5'
RESPONSE_PIN = machine.Pin(RESPONSE_PIN_NUMBER, machine.Pin.OUT, machine.Pin.PULL_DOWN)


def blinky():
    GREEN_LED.high()
    GREEN_LED.low()

def lightsleep_test(interval_in_ms, amount_of_loops):
    results = []
    run_counter = 0
    while run_counter < amount_of_loops:
        TIMER_PIN.high()
        TIMER_PIN.low()
        machine.lightsleep(interval_in_ms)
        RESPONSE_PIN.high()
        RESPONSE_PIN.low()
        run_counter += 1
    return results


"""
DEPRECATED
"""
def lightsleep_blinky_test(interval_in_ms, amount_of_loops):
    results = []
    run_counter = 0
    while run_counter < amount_of_loops:
        timer_start = utime.ticks_cpu()
        machine.lightsleep(interval_in_ms)
        timer_end = utime.ticks_cpu()
        blinky()
        results.append(utime.ticks_diff(timer_end, timer_start))
        run_counter += 1
    return results


def deepsleep_test(interval_in_ms):

    TIMER_PIN.high()
    TIMER_PIN.low()
    machine.deepsleep(interval_in_ms)

def deepsleep_blinky_test(interval_in_ms):
    timer_start = utime.ticks_cpu()
    machine.deepsleep(interval_in_ms)
    blinky()