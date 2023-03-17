import machine
import utime

STM32_CPU_CLOCK_SPEED = 64000000
GREEN_LED = machine.Pin("B0", machine.Pin.OUT)

def blinky():
    GREEN_LED.high()
    GREEN_LED.low()

def lightsleep_test(interval_in_ms, amount_of_loops):
    results = []
    run_counter = 0
    while run_counter < amount_of_loops : 
        timer_start = utime.ticks_cpu()
        machine.lightsleep(interval_in_ms)
        timer_end = utime.ticks_cpu()
        results.append([utime.ticks_diff(timer_end,timer_start)])
        run_counter += 1
    return results

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



def deepsleep_test(interval_in_ms, duration_in_ms):
    results = []
    test_start = utime.ticks_cpu()
    while utime.ticks_diff(utime.ticks_cpu(), test_start) < duration_in_ms * 1000:
        timer_start = utime.ticks_cpu()
        machine.deepsleep(interval_in_ms)
        timer_end = utime.ticks_cpu()
        results.append(utime.ticks_diff(timer_end, timer_start) - (interval_in_ms * 1000))
    return results