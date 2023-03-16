import machine
import utime


def lightsleep_test(interval_in_ms, duration_in_ms):
    print("ENTERED LIGHTSLEEP TEST")
    results = []
    test_start = utime.ticks_cpu()
    time_slept = 0
    print(test_start)
    while utime.ticks_diff(utime.ticks_cpu(), test_start) + time_slept < utime.ticks_diff(test_start + (duration_in_ms * 1000 * 64), test_start):
        print("Tick NOW:")
        print(utime.ticks_diff(utime.ticks_cpu(), test_start))
        print("TICK GOAL:")
        print(utime.ticks_diff(test_start + (duration_in_ms * 1000 * 64), test_start))
        timer_start = utime.ticks_cpu()
        machine.lightsleep(interval_in_ms)
        timer_end = utime.ticks_cpu()
        time_slept += interval_in_ms * 64
        results.append([(utime.ticks_diff(timer_end,timer_start)/64),
                        (utime.ticks_diff(timer_start,test_start)/64),
                        (utime.ticks_diff(timer_end, test_start)/64)])
        print("RESULT APPENDED")
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