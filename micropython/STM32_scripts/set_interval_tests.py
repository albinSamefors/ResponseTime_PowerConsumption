import machine
import utime

STM32_CPU_CLOCK_SPEED = 64000000

def lightsleep_test(interval_in_ms, amount_of_loops):
    print("ENTERED LIGHTSLEEP TEST")
    results = []
    test_start = utime.ticks_cpu()
    run_counter = 0
    while run_counter < amount_of_loops :
        
        timer_start = utime.ticks_cpu()
        machine.lightsleep(interval_in_ms)
        timer_end = utime.ticks_cpu()
        #print("START")
        #print(timer_start)
        #print("END")
        #print(timer_end)

        results.append([utime.ticks_diff(timer_end,timer_start),
                        utime.ticks_diff(timer_start,test_start),
                        utime.ticks_diff(timer_end, test_start)])
        run_counter += 1
    test_end = utime.ticks_cpu()
    
    return results, utime.ticks_diff(test_end, test_start)


def deepsleep_test(interval_in_ms, duration_in_ms):
    results = []
    test_start = utime.ticks_cpu()
    while utime.ticks_diff(utime.ticks_cpu(), test_start) < duration_in_ms * 1000:
        timer_start = utime.ticks_cpu()
        machine.deepsleep(interval_in_ms)
        timer_end = utime.ticks_cpu()
        results.append(utime.ticks_diff(timer_end, timer_start) - (interval_in_ms * 1000))
    return results