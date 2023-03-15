import machine
import time


def lightsleep_test(interval_in_ms, duration_in_ms):
    results = []
    test_start = time.ticks_us()
    while time.ticks_diff(time.ticks_us(), test_start) < duration_in_ms * 1000:
        timer_start = time.ticks_us()
        machine.lightsleep(interval_in_ms)
        timer_end = time.ticks_us()
        results.append(time.ticks_diff(timer_start,timer_end) - (interval_in_ms * 1000))
    return results

def deepsleep_test(interval_in_ms, duration_in_ms):
    results = []
    test_start = time.ticks_us()
    while time.ticks_diff(time.ticks_us(), test_start) < duration_in_ms * 1000:
        timer_start = time.ticks_us()
        machine.deepsleep(interval_in_ms)
        timer_end = time.ticks_us()
        results.append(time.ticks_diff(timer_start, timer_end) - (interval_in_ms * 1000))
    return results