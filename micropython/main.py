from STM32_scripts import interrupt_tests, set_interval_tests
import machine
import utime

STM32_CLOCK_FREQUENCY = 64000000
STM32_PERIOD = 1/STM32_CLOCK_FREQUENCY


def periodic_test_runner(test, data_per_run, starting_sleep_interval_ms, test_cycles=10,sleep_increase_ms=50):
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
        i += 1

def interrupt_test_runner(test):
    pass

def get_cycles_from_time(duration_s, sleep_interval_ms):
    sleep_interval_s = sleep_interval_ms/1000
    cycles = int((duration_s/sleep_interval_s))
    return cycles, sleep_interval_ms

#THIS CODE IS NOT COMPLIANT WITH DRY BUT WILL REWORKED WHEN I KNOW THAT IT WORKS
def get_test_input():
    print("----------------------TEST RUNNER----------------------")
    print("WELCOME TO THE TEST RUNNER!")
    accepted_input = False
    run_in_interrupt = True
    run_in_lightsleep = True
    peripheral_use = "none"
    start_sleep = 0
    amount_of_sleep_increases = 0
    increase_per_cycle = 0
    amount_of_runs = 0
    while not accepted_input:
        test_type = input("Do you wish to test in interrupt mode? Y/n:  ")
        if test_type.lower() == "n":
            run_in_interrupt = False
            accepted_input = True
            print("Tests will be run in Interval Mode")
        elif test_type.lower() == "y":
            accepted_input = True
            print("Tests will be run in Interrupt Mode")
        else:
            print("{} IS INVALID TRY AGAIN".format(test_type))
    accepted_input = False

    while not accepted_input:
        test_lightsleep = input("Do you wish to test Lightsleep? Y/n:   ")
        if test_lightsleep.lower() == "n":
            run_in_lightsleep = False
            print("Testing Deepsleep")
            accepted_input = True
        elif test_lightsleep.lower() == "y":
            print("Testing Lightsleep")
            accepted_input = True
        else:
            print("{} IS INVALID TRY AGAIN".format(test_lightsleep))
    accepted_input = False

    while not accepted_input:
        selected_type = input("Which function do you want to run? none, led:    ")
        if selected_type == 'led':
            accepted_input = True
            peripheral_use = selected_type
            print("LED functionality will be used")
        elif selected_type == 'none':
            accepted_input = True
            print("Raw timing will be used")
        else:
            print("{} IS INVALID TRY AGAIN".format(selected_type))
    accepted_input = False
    
    #NOT TESTED FOR NEGATIVE NUMBERS BE WARY
    if not run_in_interrupt:
        accepted_input = False
        while not accepted_input:
            raw_amount_of_runs = input("How many runs per test?:    ")
            if raw_amount_of_runs.isdigit():
                amount_of_runs = int(raw_amount_of_runs)
                accepted_input = True
                print("Will run {} times per test".format(amount_of_runs))
            else:
                print("{} IS INVALID TRY AGAIN!".format(raw_amount_of_runs))
        accepted_input = False

        while not accepted_input:
            raw_start_sleep = input("How long should the sleep start at in ms?: ")
            if raw_start_sleep.isdigit():
                start_sleep = int(raw_start_sleep)
                accepted_input = True
                print("Will increase sleep {} times per test".format(start_sleep))
            else:
                print("{} IS INVALID TRY AGAIN!".format(raw_start_sleep))
        accepted_input = False
        
        
        while not accepted_input:
            raw_amount_of_sleep_increases = input("How many increases in sleep time per test?:  ")
            if raw_amount_of_sleep_increases.isdigit():
                amount_of_sleep_increases = int(raw_amount_of_sleep_increases)
                accepted_input = True
                print("Will increase sleep {} times per test".format(amount_of_sleep_increases))
            else:
                print("{} IS INVALID TRY AGAIN!".format(raw_amount_of_sleep_increases))
        accepted_input = False

        while not accepted_input:
            raw_sleep_increase_size = input("How much should the sleep time increase per test in ms?:   ")
            if raw_sleep_increase_size.isdigit():
                increase_per_cycle = int(raw_sleep_increase_size)
                accepted_input = True
                print("Will increase sleep time each cycle with {}ms".format(increase_per_cycle))
            else:
                print("{} IS INVALID TRY AGAIN!".format(increase_per_cycle))
        func = None
        print("READY TO GO!")
        if run_in_lightsleep:
            if peripheral_use == "none":
                func = set_interval_tests.lightsleep_test
            elif peripheral_use == "led":
                func = set_interval_tests.lightsleep_blinky_test
            else:
                print("ERROR ERROR ERROR")
                
        else:
            if peripheral_use == "none":
                func = set_interval_tests.deepsleep_test
            elif peripheral_use == "led":
                func = set_interval_tests.deepsleep_blinky_test
            else:
                print("ERROR ERROR ERROR")  
        print("READY TO GO")
        periodic_test_runner(func, amount_of_runs,start_sleep,amount_of_sleep_increases,increase_per_cycle)

    else:
        print("READY TO GO!")
        interrupt_test_runner("PLACEHOLDER CHANGE THIS WHEN IMPLEMENTED")
        


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

#THESE ARE JUST HARD VALUES FOR THE RESET TYPES. 2 IS RESET BY BUTTON AND 4 IS DEEPSLEEP RESET
if machine.reset_cause() == 2:
    get_test_input()

#TODO: DEEPSLEEP TESTING IS CURRENTLY WORKING LIKE THE MOVIE MEMENTO
#EVERY TIME IT SLEEPS IT FORGETS EVERYTHING AND HAS TO START LEARNING FROM THE BEGINNING
#A POSSIBLE WAY OF HANDELNIG THIS IS TO SAVE ALL DATA INCLUDING SETUP AND HOW MANY CYCLES HAS GONE
#TO THE machine.rtc() MEMORY AND LATER PARSING THAT DATA INTO PRNTABLE RESULT
#ALTOUGHT RIGHT NOW 2023-03-18-16:57 I WONT DEAL WITH THIS.
#SO TO FUTURE ME GOOD LUCK AND DONT DO ANYTHING STUPID K ;)
elif machine.reset_cause() == 4:
    print("DEEPSLEPT")
"""
print("EXPERIMENT STARTING POINT")
cycles, sleep_interval = get_cycles_from_time(5,50)
runtime_start = utime.time()
times = set_interval_tests.lightsleep_blinky_test(sleep_interval, cycles)
runtime_end = utime.time()


pretty_print_results(times)
print("TOTAL TIME FOR RUN: {}s".format((runtime_end- runtime_start)))
"""
