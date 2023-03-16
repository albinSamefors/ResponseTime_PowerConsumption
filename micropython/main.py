from STM32_scripts import interrupt_tests, set_interval_tests
import machine
print("EXPERIMENT STARTING POINT")

times = set_interval_tests.lightsleep_test(10, 1 * 1000)

#print("MACHINE FREQ {}".format(machine.freq()))

print("ALL TIMES: \n")
for time in times:
    print("TIME: {}, Time started {}, Time Stopped {} \n".format(time[0], time[1], time[2]))