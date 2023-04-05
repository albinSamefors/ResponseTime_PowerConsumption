from STM32_scripts import interrupt_tests, set_interval_tests
import machine
import utime
import os
import uos
import sys


#SPI SETUP
RECIEVE_READY = machine.Pin('B4', machine.Pin.IN)
SS = machine.Pin('D10', mode=machine.Pin.OUT, value=1)
SCK = machine.Pin('D13', mode=machine.Pin.OUT)
MOSI = machine.Pin('D11', mode=machine.Pin.OUT)
MISO = machine.Pin('D12', mode=machine.Pin.OUT)
SPI = machine.SPI(1, baudrate=9600)
SPI.init(baudrate=9600,polarity=0,phase=0,bits=8,firstbit=SPI.MSB)

DEBUG_MODE = False

#SPI WRITE ADDS
SLEEP_TIME_SPI_ADDR =    0b00000001
RUN_AMMOUNT_SPI_ADDR =   0b00000010
TEST_MODE_SPI_ADDR =     0b00000011
SLEEP_MODE_SPI_ADDR =    0b00000100

RECIEVE_DATA_ADDR =      0b00000101
RECIEVE_PARAMS_ADDR =    0b00000110

USING_DEEPSLEEP = 1
USING_LIGHTSLEEP = 0
USING_INTERRUPTS = 1
USING_INTERVALS = 0

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

def recieve_params_SPI():
    bytesread = []
    while RECIEVE_READY.value() == 0:
        print("Waiting")
    
    try:
        SS.low()
        sleep_time = SPI.read(2, SLEEP_TIME_SPI_ADDR)
    finally:
        SS.high()
    try:
        SS.low()
        run_amount = SPI.read(2, RUN_AMMOUNT_SPI_ADDR)
    finally:
        SS.high()
    try:
        SS.low()
        test_mode = SPI.read(2, TEST_MODE_SPI_ADDR)
    finally:
        SS.high()
    try:
        SS.low()
        sleep_mode = SPI.read(2, SLEEP_MODE_SPI_ADDR)
    finally:
        SS.high
    return int.from_bytes(sleep_time, 'little'), int.from_bytes(run_amount, 'little'), int.from_bytes(test_mode, 'little'), int.from_bytes(sleep_mode, 'little')



#THESE ARE JUST HARD VALUES FOR THE RESET TYPES. 2 IS RESET BY BUTTON AND 4 IS DEEPSLEEP RESET
if machine.reset_cause() == 2:
    print("SENDING SETTINGS")
    send_settings_spi(1000, 10, 0)
    print("SETTINGS SENT, STARTING TESTS")
    set_interval_tests.lightsleep_test(1000,10)
    print("TESTS FINISHED, FETCHING DATA")
    data = recieve_data_SPI(10)
    print("DATA FETCHED!")
    sys.exit()
elif machine.reset_cause() == machine.DEEPSLEEP_RESET:
    sleep_time, run_amount, test_mode, sleep_mode = recieve_data_SPI()

