#!/usr/bin/env python
# encoding: utf-8
'''
CurrentSourceI2C.py
Created on Oct 7, 2014
@author: Michael Empey
'''

import sys, SCPI, time
import numpy as np
from I2C import *
from Digital_Potentiometer import *

''' SCRIPT PARAMETERS '''
#port = "/dev/tty.usbserial-A1017JW6"
port = "/dev/ttyUSB0"
speed = 115200

save_file_name = "Data/200k_pot_range_test.csv"

R1 = Digital_Potentiometer(0,0,0,200e3)
R2 = Digital_Potentiometer(0,0,1,200e3)

totalSamples = "INF"
sampleFreq = 100000

freq    = SCPI.SCPI("192.168.2.1")
resist_meter = SCPI.SCPI("192.168.2.2")
# voltage = SCPI.SCPI("192.168.2.2")
# current = SCPI.SCPI("192.168.2.3")


''' UTILITY FUNCTIONS '''
def i2c_write_data(data, resp=True):
    error = 0
    addr = data[0]
    i2c.send_start_bit()
    for i in data:
        status = i2c.bulk_trans(1, [i])
        if(resp):
            if status.find(chr(0x01)) != -1:

                error = 1
    i2c.send_stop_bit()
    print [hex(x) for x in data]
    if error:
        print "I2C command not acknowledged!"
        print [hex(x) for x in data]
        print "Reset Bus Pirate to user terminal: "
        if i2c.resetBP():
            print "OK."
        else:
            print "failed."
        sys.exit()

''' MAIN PROGRAM '''
if __name__ == '__main__':

    ''' Set up DMMs '''
    # setup freq gen
    freq.setSquare()
    freq.setVoltage(0,3)
    freq.setFrequency(sampleFreq)

    # setup resistance meter
    resist_meter.setResistance("AUTO", "MAX")
    resist_meter.setTriggerSource()
    resist_meter.setTriggerCount(totalSamples)
    resist_meter.setInitiate()

    time.sleep(1)

    freq.setOutput(1)


    ''' Set up bus pirate '''
    i2c = I2C(port, speed)

    print "Entering binmode: ",
    if i2c.BBmode():
        print "OK."
    else:
        print "failed."
        print "retrying..."
        i2c.port.write("\x0d\x0d\x0d\x0d\x0d\x0d\x0d\x0d\x0d\x0d")
        i2c.port.write("\x23")
        if i2c.BBmode():
            print "OK."
        else:
            print "failed. again..."
        sys.exit()

    print "Entering raw I2C mode: ",
    if i2c.enter_I2C():
        print "OK."
    else:
        print "failed."
        sys.exit()

    print "Configuring I2C."
    if not i2c.cfg_pins(I2CPins.POWER | I2CPins.PULLUPS):
#     if not i2c.cfg_pins(I2CPins.PULLUPS):
        print "Failed to set I2C peripherals."
        sys.exit()
    if not i2c.set_speed(I2CSpeed._50KHZ):
        print "Failed to set I2C Speed."
        sys.exit()
    i2c.timeout(0.2)


    ''' Experiment Code '''
    print "Loop Through Pot Values"
    for ii in range(0,256):
        i2c_write_data(R1.I2C_set_value(ii))
        time.sleep(0.0001)
        r_meas_meter = resist_meter.getMeasurements()
        r_meas = np.mean(r_meas_meter[-5:])
        r_ideal = R1.get_ideal_value()
        r_tmp = [ii, r_ideal, r_meas]
        print r_tmp
        if ii == 0:
            r_data = np.array([r_tmp])
        else:
            r_data = np.append(r_data,[r_tmp], 0)

    print r_data
    np.savetxt(save_file_name, r_data, delimiter=',', fmt='%.2f')

#     input("Press Enter to continue...")

    ''' Experiment Done Reset Bus Pirate '''
    print "Reset Bus Pirate to user terminal: "
    if i2c.resetBP():
        print "OK."
    else:
        print "failed."
    sys.exit()




