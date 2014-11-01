import sys
import SCPI
import time
#import numpy

totalSamples = "INF"
sampleFreq = 100000

freq    = SCPI.SCPI("192.168.2.1")
voltage = SCPI.SCPI("192.168.2.2")
current = SCPI.SCPI("192.168.2.3")

#setup freq gen
freq.setSquare()
freq.setVoltage(0,3)
freq.setFrequency(sampleFreq)

#setup voltage meter
voltage.setVoltageDC("10V", "MAX")
# set external trigger
voltage.setTriggerSource()
voltage.setTriggerCount(totalSamples)
# wait for trigger
voltage.setInitiate()

current.setCurrentDC("1A", "MAX")
current.setTriggerSource()
current.setTriggerCount(totalSamples)
current.setInitiate()

time.sleep(1)

freq.setOutput(1)

currentMeasurements = []
voltageMeasurements = []
j = 0

while 1:

    currentMeasurements += current.getMeasurements()
    voltageMeasurements += voltage.getMeasurements()

    l = min(len(currentMeasurements), len(voltageMeasurements))

    for i in range(l):
        print j, float(j)/float(sampleFreq), currentMeasurements[i], voltageMeasurements[i]
        j += 1
    currentMeasurements = currentMeasurements[l-1]
    voltageMeasurements = voltageMeasurements[l:-1]

    sys.stdout.flush()

    time.sleep(0.5)
