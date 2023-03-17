from STM32_scripts import interrupt_tests, set_interval_tests
import machine
import utime

STM32_CLOCK_FREQUENCY = 64000000
STM32_PERIOD = 1/STM32_CLOCK_FREQUENCY


def periodic_test_runner(test, data_per_run, starting_sleep_interval_ms, test_cycles=10,sleep_increase_ms=50):
    input("Press ENTER TO START TESTING")
    counter = 0
    results = []
    sleep_interval = starting_sleep_interval_ms
    while counter < test_cycles:
        print("Running test {} of {}".format((counter+1), test_cycles))
        times = test(sleep_interval, data_per_run)
        results.append(times)
        sleep_interval += sleep_increase_ms
        counter += 1
    i=0
    for result in results:
        pretty_print_results(result, (starting_sleep_interval_ms + (sleep_increase_ms * i)))
        i +=1






def get_cycles_from_time(duration_s, sleep_interval_ms):
    sleep_interval_s = sleep_interval_ms/1000
    cycles = int((duration_s/sleep_interval_s))
    return cycles, sleep_interval_ms

def pretty_print_results(results, sleep_interval):
    def avg_us(results):
        avg_cycles = sum(results) / len(results)
        avg_time = avg_cycles * STM32_PERIOD * 1000 * 1000
        return avg_time
    print("-----------------------TEST STATS-----------------------")
    print("Sleep interval ms:              {}".format(sleep_interval))
    print("Amount of collected data:       {}".format(len(results)))
    print("Average response time us:       {}".format(avg_us(results)))
    print("Fastest response time us:       {}".format(min(results) * STM32_PERIOD * 1000 * 1000))
    print("Slowest response time us:       {}".format(max(results) * STM32_PERIOD * 1000 * 1000))
    print("--------------------------------------------------------")

periodic_test_runner(set_interval_tests.lightsleep_blinky_test,100,1,20,1)
"""
print("EXPERIMENT STARTING POINT")
cycles, sleep_interval = get_cycles_from_time(5,50)
runtime_start = utime.time()
times = set_interval_tests.lightsleep_blinky_test(sleep_interval, cycles)
runtime_end = utime.time()


pretty_print_results(times)
print("TOTAL TIME FOR RUN: {}s".format((runtime_end- runtime_start)))
"""
