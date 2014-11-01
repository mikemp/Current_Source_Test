#!/usr/bin/env python
# encoding: utf-8
'''
Current Src Breakout Test
Note: A 0x00 position for the pots is the Max

Created on Nov 1, 2014
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

save_file_trans = "current_src_confA_trans"
save_file_steady = "current_src_confA_steady"
ext = "csv"

R1A = Digital_Potentiometer(0,0,0,200e3)
R1B = Digital_Potentiometer(0,0,1,200e3)
R2A = Digital_Potentiometer(1,0,0,200e3)
R2B = Digital_Potentiometer(1,0,1,200e3)
R3A = Digital_Potentiometer(1,1,0,1e6)

totalSamples = "INF"
sampleFreq = 100000

freq    = SCPI.SCPI("192.168.2.1")
# resist_meter = SCPI.SCPI("192.168.2.2")
voltage = SCPI.SCPI("192.168.2.2")
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
        
def r_par_eq(R1A,R1B):
    return R1A*R1B/(R1A+R1B)

''' MAIN PROGRAM '''
if __name__ == '__main__':

    ''' Set up DMMs '''
    # setup freq gen
    freq.setSquare()
    freq.setVoltage(0,3)
    freq.setFrequency(sampleFreq)

#     # setup resistance meter
#     resist_meter.setResistance("10000000", "MAX")
#     #resist_meter.setAutoInputImpedance("ON")
#     resist_meter.setTriggerSource()
#     resist_meter.setTriggerCount(totalSamples)
#     resist_meter.setInitiate()

    #setup voltage meter
    voltage.setVoltageDC("10V", "MAX")
    voltage.setTriggerSource()
    voltage.setTriggerCount(totalSamples)
    voltage.setInitiate()
    
#     #setup current meter
#     current.setCurrentDC("1A", "MAX")
#     current.setTriggerSource()
#     current.setTriggerCount(totalSamples)
#     current.setInitiate()

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
    # Shutdown R2 and R3
    i2c_write_data(R2A.shutdown())
    i2c_write_data(R2B.shutdown())
    i2c_write_data(R3A.shutdown())
    
    print "Loop Through Pot Values"
    #for ii in range(0,256):
    for ii in range(255,-1,-1): # reversed
        # clear DMM measurements
        meas_dump = voltage.getMeasurements()
        # set pots to the same value
        i2c_write_data(R1A.I2C_set_value(ii))
        i2c_write_data(R1B.I2C_set_value(ii))
        
        # wait for transient response
        time.sleep(0.001)
        
        # record DMM voltages as transient response
        trans_resp = voltage.getMeasurements(); 
        steady_state = np.mean(trans_resp[-5:])
        
        # save transient response into file
        sample_base = range(0,len(trans_resp))
        time_base = [float(x)/float(sampleFreq) for x in sample_base]
        trans_data = np.array(sample_base,time_base,trans_resp)
        trial = "%04d" % (ii)
        np.savetxt("%s_%s.%s" % (save_file_trans,trial,ext), trans_data, delimiter=',', fmt='%.6f')
        
        # record steady state into array
        r_ideal = r_par_eq(R1A.get_ideal_value(),R1B.get_ideal_value())
        r_tmp = [ii, r_ideal, steady_state]
        print r_tmp
        if ii == 0:
            steady_data = np.array([r_tmp])
        else:
            steady_data = np.append(steady_data,[r_tmp], 0)

#     print steady_data
    np.savetxt("%s.%s" % (save_file_steady,ext), steady_data, delimiter=',', fmt='%.6f')

#     input("Press Enter to continue...")

    ''' Experiment Done Reset Bus Pirate '''
    print "Reset Bus Pirate to user terminal: "
    if i2c.resetBP():
        print "OK."
    else:
        print "failed."
    sys.exit()


