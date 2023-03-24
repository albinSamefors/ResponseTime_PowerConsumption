import machine

TIMER_PIN_NUMBER = 'A0'
TIMER_PIN = machine.Pin(TIMER_PIN_NUMBER, machine.Pin.OUT, machine.Pin.PULL_DOWN)
IRQ_PIN_NUMBER = 'A1'
IRQ_PIN = machine.Pin(IRQ_PIN_NUMBER, machine.Pin.IN, machine.Pin.PULL_DOWN)

def timer_signal():
    TIMER_PIN.on()
    TIMER_PIN.off()

def lightsleep_test():
    IRQ_PIN.irq(trigger=machine.IRQ_RISING, handler=timer_signal)
    machine.lightsleep()

def deepsleep_test():
    IRQ_PIN.irq(trigger=machine.IRQ_RISING, handler=timer_signal)
    machine.deepsleep()
