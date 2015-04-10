#!/usr/bin/env python
# encoding: utf-8
'''
Current Source Version 3 Breakout Test
Config 1:


@author: Michael Empey
'''

import sys, SCPI, time
import numpy as np
from BinaryMode.SPI import *

''' SCRIPT PARAMETERS '''
#port = "/dev/tty.usbserial-A1017JW6"
port = "/dev/ttyUSB0"
speed = 115200

totalSamples = "INF"
sampleFreq = 100000

freq    = SCPI.SCPI("192.168.2.1")
current = SCPI.SCPI("192.168.2.3")


''' UTILITY FUNCTIONS '''
def print_i2c(data):
    print [hex(x) for x in data]


''' MAIN PROGRAM '''
if __name__ == '__main__':

    ''' Set up DMMs '''
    # setup freq gen
    freq.setSquare()
    freq.setVoltage(0,3)
    freq.setFrequency(sampleFreq)

    #setup current meter
    current.setCurrentDC("10mA", "MAX")
    current.setTriggerSource()
    current.setTriggerCount(totalSamples)
    current.setInitiate()

    time.sleep(1)

    freq.setOutput(1)


    ''' Set up bus pirate '''
    spi = SPI(port, speed)

    print "Entering binmode: ",
    if spi.BBmode():
        print "OK."
    else:
        print "failed."
        sys.exit()

    print "Entering raw SPI mode: ",
    if spi.enter_SPI():
        print "OK."
    else:
        print "failed."
        sys.exit()
        
    print "Configuring SPI."
    if spi.cfg_pins(PinCfg.POWER | PinCfg.CS | PinCfg.AUX):
        print "Failed to set SPI peripherals."
        sys.exit()
    if spi.set_speed(SPISpeed._2_6MHZ):
        print "Failed to set SPI Speed."
        sys.exit()
    if spi.cfg_spi(SPICfg.CLK_EDGE | SPICfg.OUT_TYPE):
        print "Failed to set SPI configuration.";
        sys.exit()
    spi.timeout(0.2)


set_current = 1



    ''' Experiment Done Reset Bus Pirate '''
    print "Reset Bus Pirate to user terminal: "
    if i2c.resetBP():
        print "OK."
    else:
        print "failed."
    sys.exit()


