#!/usr/bin/env python
# encoding: utf-8
'''
CurrentSourceI2C.py
Created on Oct 7, 2014
@author: Michael Empey
'''

import sys, SCPI, time
from I2C import *
from Digital_Potentiometer import *

''' SCRIPT PARAMETERS '''
port = "/dev/tty.usbserial-A1017JW6"
speed = 115200

R1 = Digital_Potentiometer(0,0,0)
R2 = Digital_Potentiometer(0,0,1)


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
    
    

    i2c_write_data(R1.I2C_set_value(20))

    print "Reset Bus Pirate to user terminal: "
    if i2c.resetBP():
        print "OK."
    else:
        print "failed."
    sys.exit()