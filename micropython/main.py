from STM32_scripts import interrupt_tests, set_interval_tests
import machine
import utime
import os

STM32_CLOCK_FREQUENCY = 64000000
STM32_PERIOD = 1/STM32_CLOCK_FREQUENCY

def lightsleep_test_runner(test, data_per_run, sleep_interval_ms):
    print("RUNNING LIGHTSLEEP TEST")
    time_now = utime.gmtime()
    timestamp = str(time_now[0]) + str(time_now[1]) + str(time_now[2]) + str(time_now[3]) + str(time_now[4]) + str(time_now[5])
    file_name = test.__name__ +"_sleep_interval_ms_"+ str(sleep_interval_ms) + "_" + str(timestamp) + ".txt"
    os.chdir('lightsleep_test_data')
    file = open(file_name, 'w+')
    cycles = test(sleep_interval_ms, data_per_run)
    for cycle in cycles:
        file.write(str(cycle * STM32_PERIOD * 1000 * 1000) + "\n")
    file.close()
    print("DATA STORED IN FILE: {}".format(file_name))
    load_and_print_data(file_name)

def deepsleep_test_runner(test, data_per_run, sleep_interval_ms):

    # RESET CAUSE 4 IMPLIES A DEEP SLEEP RESET
    if machine.reset_cause() != 4:
        #SENDING WELCOME MESSAGE IF THE USER RESTARTED THE MCU
        time_now = utime.gmtime()
        timestamp = str(time_now[0]) + str(time_now[1]) + str(time_now[2]) + str(time_now[3]) + str(time_now[4]) + str(time_now[5])
        file_name = test.__name__ +"_sleep_interval_ms_"+ str(sleep_interval_ms) + "_" + str(timestamp) + ".txt"
        os.chdir('deepsleep_test_data')
        #file = open(file_name, 'a')
        #file.close()
        print("RUNNING DEEPSLEEP TEST")
        rtc = machine.RTC()
        #SAVING DATA TO THE STATIC RTC RAM TO BE ABLE TO KEEP RUNNING THE TEST
        rtc.memory([file_name, test, data_per_run, sleep_interval_ms, 0])
        test()
    else:
        end_time = utime.ticks_cpu()
        print("DEATH")
        #THE MCU WAS RESETTED BY DEEPSLEEP CHECK FIRST LINE
        pass
        

def interrupt_test_runner(test):
    pass

def get_cycles_from_time(duration_s, sleep_interval_ms):
    sleep_interval_s = sleep_interval_ms/1000
    cycles = int((duration_s/sleep_interval_s))
    return cycles, sleep_interval_ms

def load_and_print_data(file_name):
    file = open(file_name, 'r')
    results = []
    for line in file.readlines():
        results.append(float(line))
    print("-----------------------TEST STATS-----------------------")
    print("Amount of collected data:       {}".format(len(results)))
    print("Average response time us:       {}".format((sum(results)/len(results))))
    print("Fastest response time us:       {}".format(min(results)))
    print("Slowest response time us:       {}".format(max(results)))
    print("--------------------------------------------------------")

    file.close()

#THESE ARE JUST HARD VALUES FOR THE RESET TYPES. 2 IS RESET BY BUTTON AND 4 IS DEEPSLEEP RESET
if machine.reset_cause() == 2:
    lightsleep_test_runner(set_interval_tests.lightsleep_test,1000,10)

#TODO: DEEPSLEEP TESTING IS CURRENTLY WORKING LIKE THE MOVIE MEMENTO
#EVERY TIME IT SLEEPS IT FORGETS EVERYTHING AND HAS TO START LEARNING FROM THE BEGINNING
#A POSSIBLE WAY OF HANDELNIG THIS IS TO SAVE ALL DATA INCLUDING SETUP AND HOW MANY CYCLES HAS GONE
#TO THE machine.rtc() MEMORY AND LATER PARSING THAT DATA INTO PRNTABLE RESULT
#ALTOUGHT RIGHT NOW 2023-03-18-16:57 I WONT DEAL WITH THIS.
#SO TO FUTURE ME GOOD LUCK AND DONT DO ANYTHING STUPID K ;)
elif machine.reset_cause() == 4:
    print("DEEPSLEPT")

