'''
Created on Apr 10, 2015

@author: mikemp
'''

import sys
import SCPI
import time
#import numpy

totalSamples = "INF"
sampleFreq = 100000

freq    = SCPI.SCPI("192.168.2.1")
current = SCPI.SCPI("192.168.2.2")

#setup freq gen
freq.setSquare()
freq.setVoltage(0,3)
freq.setFrequency(sampleFreq)


current.setCurrentDC("10mA", "MAX")
current.setTriggerSource()
current.setTriggerCount(totalSamples)
current.setInitiate()

time.sleep(1)

freq.setOutput(1)

currentMeasurements = []
j = 0

while 1:

    currentMeasurements += current.getMeasurements()

    l = min(len(currentMeasurements))

    for i in range(l):
        print j, float(j)/float(sampleFreq), currentMeasurements[i]
        j += 1
    currentMeasurements = currentMeasurements[l-1]

    sys.stdout.flush()

    time.sleep(0.5)
