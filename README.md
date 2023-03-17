# Investigating Energy Consumption and Responsiveness of MicroPython in Embedded Systems
## Bachelor thesis work by Albin Samefors and Felix Sundman
This repository holds the code used to test the energy consumption and responsiveness in both C and MicroPython.

## Description of folders
### C 
Contains test code for the C programming language
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

#### Internal led pins
Setup:
```
from machine import Pin

green_led = Pin("B0", Pin.OUT)
red_led = Pin("B1", Pin.OUT)

#To turn on led
green_led.high()
#To turn off led
green_led.low()

```
### controller
Contains the code for the controller part of the test platform. The purpose of this is to have an indipendent measuring device to not burden the test mcu more than neccesary to ensure that the data collected is accurate.
### measurments
Contains all the measurments taken from the experiments
