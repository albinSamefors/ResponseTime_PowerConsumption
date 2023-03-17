from STM32_scripts import interrupt_tests, set_interval_tests
import machine
import utime


def get_cycles_from_time(duration_s, sleep_interval_ms):
    sleep_interval_s = sleep_interval_ms/1000
    cycles = int((duration_s/sleep_interval_s))
    return cycles, sleep_interval_ms


print("EXPERIMENT STARTING POINT")
cycles, sleep_interval = get_cycles_from_time(5,50)
runtime_start = utime.time()
times = set_interval_tests.lightsleep_test(sleep_interval, cycles)
runtime_end = utime.time()

print("ALL TIMES: \n")
for time in times:
    print("CYCLES: {}\n".format(time[0]))
    print("TIME: {} us".format((time[0] * 1/64000000) * 1000 * 1000 ))

print("Ammount of collected data  {}".format(len(times)))

print("TOTAL TIME FOR RUN: {}s".format((runtime_end- runtime_start)))

