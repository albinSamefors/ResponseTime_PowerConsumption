import numpy as np
import glob
import os

LIGHTSLEEP_INTERVAL_FOLDER = "Lightsleep_Interval"
LIGHTSLEEP_INTERRUPT_FOLDER = "Lightsleep_Interrupt"
DEEPSLEEP_INTERVAL_FOLDER = "Deepsleep_Interval"
DEEPSLEEP_INTERRUPT_FOLDER = "Deepsleep_Interrupt"

def loadFolder(folderName):
    all_files = []
    for root, dirs, files in os.walk(folderName, topdown=False):
        for name in files:
            all_files.append(open(folderName + "/" + name))
    return all_files

def findErrorMargin(inputFile):
    period = 16/32768
    string_sleep_in_ms = ""
    for c in inputFile.name:
        if c.isdigit():
            string_sleep_in_ms += c
    sleep_in_ms = int(string_sleep_in_ms)
    sleep_in_s = sleep_in_ms / 1000
    sleeptime = (sleep_in_s / period)
    rounded_sleep = round(sleeptime)
    difference = sleeptime - rounded_sleep
    difference_in_us = (difference * period) * 1000000
    return difference_in_us

def load_and_adjust_data(datafile, adjustment):
    data = []
    i = 0
    print(datafile)
    for line in datafile.readlines():
        print("NO {}".format(i))
        print(line)
        value = int(line) + adjustment
        data.append(value)
        i += 1
    return data

def get_mean(data):
    np_arr = np.array(data)
    return np_arr.mean()

def get_standard_deviation(data):
    return np.std(data)

def main():
    files = loadFolder(DEEPSLEEP_INTERVAL_FOLDER)
    data = []
    for i in range(len(files)):
        #difference_in_us = findErrorMargin(files[i])
        data.append(load_and_adjust_data(files[i], 0))
    j = 0
    for block in data:
        print("FILE :{} \n MEAN: {} \n STANDARD DEVIATION: {} \n".format(files[j].name, get_mean(block), get_standard_deviation(block)))
        j+=1
if __name__ == "__main__":
    main()