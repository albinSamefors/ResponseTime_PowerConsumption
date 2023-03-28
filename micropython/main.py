from STM32_scripts import interrupt_tests, set_interval_tests
import machine
import utime
import os
import uos
import sys
RECIEVE_READY = machine.Pin('B4', machine.Pin.IN)
SS = machine.Pin('D10', mode=machine.Pin.OUT, value=1)
SCK = machine.Pin('D13', mode=machine.Pin.OUT)
MOSI = machine.Pin('D11', mode=machine.Pin.OUT)
MISO = machine.Pin('D12', mode=machine.Pin.OUT)
SPI = machine.SPI(1, baudrate=9600)
SPI.init(baudrate=9600,polarity=0,phase=0,bits=8,firstbit=SPI.MSB)

SLEEP_TIME_SPI_ADDR =    0b00000001
RUN_AMMOUNT_SPI_ADDR =   0b00000010
TEST_MODE_SPI_ADDR =     0b00000011
RECIEVE_DATA_ADDR =      0b00000100


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

def send_settings_spi(sleep_time, run_amount, run_type):
    """
    It takes in three parameters, sleep_time, run_amount, and run_type, and sends them to the
    microcontroller via SPI
    
    :param sleep_time: The time in seconds the system will sleep
    :param run_amount: The number of times the test will run
    :param run_type: 0 = Interval mode, 1 = Interrupt mode
    """
    try:
        timearr = sleep_time.to_bytes(2,'little')
        SS.low()
        SPI.write(bytearray([SLEEP_TIME_SPI_ADDR,
                             timearr[0],
                             timearr[1]]))
    finally:
        SS.high()
    try:
        amountarr = run_amount.to_bytes(2,'little')
        SS.low()
        SPI.write(bytearray([RUN_AMMOUNT_SPI_ADDR,
                             amountarr[0],
                             amountarr[1]]))
    finally:
        SS.high()


    try:
        typearr = run_type.to_bytes(2,'little')
        SS.low()
        SPI.write(bytearray([TEST_MODE_SPI_ADDR,
                            typearr[0],
                            typearr[1]]))
    finally:
        SS.high()

def recieve_data_SPI(run_amount):
    bytesread = []
    print("PIN VALUE {}".format(RECIEVE_READY.value()))
    while RECIEVE_READY.value() == 0:
        print("WAITING")
    for i in range(run_amount*2):
        try:
            SS.low()
            spi_data = SPI.read(2, RECIEVE_DATA_ADDR)
            bytesread.append(spi_data)
        finally:
            SS.high()
    datasetLOL = []
    for i in range(len(bytesread)):
        if i % 2 == 0:
            pass
        else:
            datasetLOL.append(int.from_bytes(bytesread[i], "little"))
    for byte in datasetLOL:
        print("VALUE: {}".format(byte))

    print(len(datasetLOL))
    return spi_data


#THESE ARE JUST HARD VALUES FOR THE RESET TYPES. 2 IS RESET BY BUTTON AND 4 IS DEEPSLEEP RESET
if machine.reset_cause() == 2:
    send_settings_spi(10, 500, 1)
    set_interval_tests.lightsleep_test(10,500)
    data = recieve_data_SPI(500)
    sys.exit()
elif machine.reset_cause() == 4:
    print("DEEPSLEPT")

