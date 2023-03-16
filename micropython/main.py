from STM32_scripts import interrupt_tests, set_interval_tests
import machine
import utime

print("EXPERIMENT STARTING POINT")
runtime_start = utime.time()
times, total_cycles = set_interval_tests.lightsleep_test(10, 1000)
runtime_end = utime.time()
#print("MACHINE FREQ {}".format(machine.freq()))

print("ALL TIMES: \n")
for time in times:
    print("CYCLES: {}, Tick started {}, Tick Stopped {} \n".format(time[0], time[1], time[2]))
    print("TIME: {} us".format((time[0] * 1/64000000) * 1000 * 1000 ))

print("TOTAL TIME FOR RUN: {}s".format((runtime_end- runtime_start)))