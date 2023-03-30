import machine
import utime
IRQ_PIN = machine.Pin('A1', machine.Pin.IN, machine.Pin.PULL_DOWN)
TIMER_PIN_NUMBER = 'A0'
TIMER_PIN = machine.Pin(TIMER_PIN_NUMBER, machine.Pin.OUT, machine.Pin.PULL_DOWN)
RESPONSE_PIN_NUMBER = 'A5'
RESPONSE_PIN = machine.Pin(RESPONSE_PIN_NUMBER,machine.Pin.OUT, machine.Pin.PULL_DOWN)
captures = 0

RUN_EXPERIMENT = True
def send_start_signal():
    TIMER_PIN.high()
    TIMER_PIN.low()

def send_stop_signal():
    RESPONSE_PIN.high()
    RESPONSE_PIN.low()
   

def callback(pin):
    RESPONSE_PIN.high()
    RESPONSE_PIN.low()
    global captures
    captures +=1


IRQ_PIN.irq(trigger=machine.Pin.IRQ_RISING, handler=callback)

def lightsleep_test(amount_of_runs):
    global captures
    while True:
        if(captures == amount_of_runs):
            break
        send_start_signal()
        print("WENT TO SLEEP round {} of {}".format(captures, amount_of_runs))
        machine.lightsleep()
        print("WOKE UP round {} of {}".format(captures, amount_of_runs))
    print("EXITED FUNCTION")
        
