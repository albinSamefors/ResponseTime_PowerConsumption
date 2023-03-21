# Investigating Energy Consumption and Responsiveness of MicroPython in Embedded Systems
## Bachelor thesis work by Albin Samefors and Felix Sundman
This repository holds the code used to test the energy consumption and responsiveness in both C and MicroPython.

## Description of folders
### C 
Contains test code for the C programming language

#### TLDR Code explanation
This code is for a STM32WB55RG microcontroller that receives data over I2C and enters sleep mode using low-power regulator when the data is received. After waking up from sleep mode, the code blinks an LED for a certain period of time and then goes back to sleep.

The main function sets up the necessary peripherals, initializes some variables, and enters an infinite loop. Inside the loop, the code waits for data to be received over I2C using the function HAL_I2C_Slave_Receive_IT(). When data is received, the microcontroller enters stop mode using the HAL_PWR_EnterSTOPMode() function and enables the low-power regulator. After waking up from stop mode, the code blinks the LED using the blink_led() function and then goes back to waiting for data over I2C.

The SystemClock_Config() function configures the system clock using the RCC (Reset and Clock Control) peripheral. It sets up the internal and external oscillators and selects the HSE (High Speed External) oscillator as the system clock source.

The MX_GPIO_Init() function initializes the GPIO (General Purpose Input/Output) peripheral. It sets up the LED pin as an output and sets its initial state to high.

The MX_I2C1_Init() function initializes the I2C1 peripheral. It sets up the I2C clock speed and the I2C address that the microcontroller will respond to as a slave device.

The MX_RTC_Init() function initializes the RTC (Real-Time Clock) peripheral. This function is not used in the code.

Overall, the code is designed to minimize power consumption by putting the microcontroller in sleep mode when it is not actively receiving data.

### micropython
Contains test code for the micropython programming language

#### To access the micropython system with rshell:
To connect to device:
```
> rshell

rshell> connect serial "PORT" "BAUDRATE" //Standard port is /dev/ttyACM0: Standard baudrate: 115200
```
To load new code

```
rshell> cp file_to_transfer.py /pyboard/flash/ // Transfers a single file
rshell> cp -r folder_to_transfer /pyboard/flash //Transfers entire folder
```
To enter REPL
```
rshell> repl
```
Exit repl by using CTRL-X
### controller
Contains the code for the controller part of the test platform. The purpose of this is to have an indipendent measuring device to not burden the test mcu more than neccesary to ensure that the data collected is accurate.
### measurments
Contains all the measurments taken from the experiments
