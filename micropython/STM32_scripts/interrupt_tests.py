import machine
import pyb
IRQ_PIN = pyb.Pin('A1', pyb.Pin.IN, pyb.Pin.PULL_DOWN) 
IRQ_TRIGGER = pyb.ExtInt.IRQ_RISING

TIMER_PIN_NUMBER = 'A0'
TIMER_PIN = machine.Pin(TIMER_PIN_NUMBER, machine.Pin.OUT, machine.Pin.PULL_DOWN)

def timer_signal():
    TIMER_PIN.on()
    TIMER_PIN.off()

IRQ = pyb.ExtInt(IRQ_PIN,IRQ_TRIGGER,pyb.Pin.PULL_NONE, timer_signal)
def lightsleep_test():
    pyb.wfi()

def deepsleep_test():
    pyb.stop() 