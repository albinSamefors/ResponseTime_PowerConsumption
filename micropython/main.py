from STM32_scripts import interrupt_tests, set_interval_tests
import machine
import utime
import os
import uos
import sys
RECIEVE_READY = machine.Pin('B4', machine.Pin.IN)

FIRSTRUNDONE = machine.Pin('A3', machine.Pin.IN)

SS = machine.Pin('D10', mode=machine.Pin.OUT, value=1)
SCK = machine.Pin('D13', mode=machine.Pin.OUT)
MOSI = machine.Pin('D11', mode=machine.Pin.OUT)
MISO = machine.Pin('D12', mode=machine.Pin.OUT)
SPI = machine.SPI(1, baudrate=9600)
SPI.init(baudrate=9600,polarity=0,phase=0,bits=8,firstbit=SPI.MSB)

DEBUG_MODE = False

SLEEP_TIME_SPI_ADDR =    0b00000001
RUN_AMMOUNT_SPI_ADDR =   0b00000010
TEST_MODE_SPI_ADDR =     0b00000011
RECIEVE_DATA_ADDR =      0b00000100

SLEEPTIME = 1000
RUN_AMOUNT = 100
WAKEUP_TYPE = 0


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
        if(DEBUG_MODE):
            sys.exit()
        else:
            print("Waiting")

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

doing_run = False
#THESE ARE JUST HARD VALUES FOR THE RESET TYPES. 2 IS RESET BY BUTTON AND 4 IS DEEPSLEEP RESET
#print(machine.reset_cause())
if machine.reset_cause() == 2 and (FIRSTRUNDONE.value() == 0 or WAKEUP_TYPE == 0):
    #print("SENDING SETTINGS")
    send_settings_spi(SLEEPTIME, RUN_AMOUNT, WAKEUP_TYPE)
    #print("SETTINGS SENT, STARTING TESTS")
    set_interval_tests.lightsleep_test(SLEEPTIME,RUN_AMOUNT)
    #interrupt_tests.lightsleep_test(100)
    #print("GOING TO SLEEP")
    #set_interval_tests.deepsleep_test(SLEEPTIME)
    #print("WOKE UP FROM SLEEP")
    #interrupt_tests.deepsleep_test()
    #print("TESTS FINISHED, FETCHING DATA")
    data = recieve_data_SPI(100)
    #print("DATA FETCHED!")
    #sys.exit()
elif machine.reset_cause() == 4 or FIRSTRUNDONE.value() == 1:
    #print("DEEPSLEPT")
    if WAKEUP_TYPE == 0:
        set_interval_tests.RESPONSE_PIN.high()
        set_interval_tests.RESPONSE_PIN.low()
        set_interval_tests.deepsleep_test(SLEEPTIME)
        #print("INTERVAL DEEPSLEEP")
    else:
        #print("RESPONDING TO INTERRUPT")
        interrupt_tests.RESPONSE_PIN.high()
        interrupt_tests.RESPONSE_PIN.low()
        interrupt_tests.deepsleep_test()

