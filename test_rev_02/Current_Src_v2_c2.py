#!/usr/bin/env python
# encoding: utf-8
'''
Current Source Version 2 Breakout Test
Configureation 2:


Created on Nov 1, 2014
@author: Michael Empey
'''

import sys, SCPI, time
import numpy as np
from I2C import *
from Digital_Potentiometer import *
from Digital_Pot_Group import *

''' SCRIPT PARAMETERS '''
#port = "/dev/tty.usbserial-A1017JW6"
port = "/dev/ttyUSB0"
speed = 115200

save_file_trans = "current_src_confA_trans"
save_file_steady = "current_src_v2_conf1_steady"
ext = "csv"

R1 = Digital_Potentiometer(0, 0, 0, 0, 1E3)
R2 = Digital_Potentiometer(0, 0, 0, 1, 1E3)
R3 = Digital_Potentiometer(0, 0, 1, 0, 1E3)
R4 = Digital_Potentiometer(0, 0, 1, 1, 1E3)

R5 = Digital_Potentiometer(0, 1, 0, 0, 1E3)
R6 = Digital_Potentiometer(0, 1, 0, 1, 1E3)
R7 = Digital_Potentiometer(0, 1, 1, 0, 1E3)
R8 = Digital_Potentiometer(0, 1, 1, 1, 1E3)

R9  = Digital_Potentiometer(1, 1, 0, 0, 1E3)
R10 = Digital_Potentiometer(1, 1, 0, 1, 1E3)
R11 = Digital_Potentiometer(1, 1, 1, 0, 1E3)
R12 = Digital_Potentiometer(1, 1, 1, 1, 1E3)

RG1 = Digital_Pot_Group([R9,R1,R2,R3,R4])
RG2 = Digital_Pot_Group([R10,R11,R12,R5,R6,R7,R8])

totalSamples = "INF"
sampleFreq = 100000

freq    = SCPI.SCPI("192.168.2.1")
# resist_meter = SCPI.SCPI("192.168.2.2")
voltage = SCPI.SCPI("192.168.2.2")
current = SCPI.SCPI("192.168.2.3")


''' UTILITY FUNCTIONS '''
def print_i2c(data):
#     print data
    print [hex(x) for x in data]

def i2c_group_write_data(pot_group, resp=True, display=True):
    pot_array = pot_group.get_pots()
    if display == True:
        i2c_group_print_data(pot_group)
    for pot in pot_array:
        i2c_write_data(pot.I2C_set_command(), resp, display=False)

def i2c_group_print_data(pot_group):
    pot_array = pot_group.get_pots()
    ic2_command = []
    for pot in pot_array:
        ic2_command.append([hex(x) for x in pot.I2C_set_command()])
    print ic2_command

def i2c_write_data(data, resp=True, display=True):
    error = 0
    addr = data[0]
    i2c.send_start_bit()
    for i in data:
        status = i2c.bulk_trans(1, [i])
        if(resp):
            if status.find(chr(0x01)) != -1:
                error = 1
    i2c.send_stop_bit()
    if display:
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

# def i2c_group_write_data(pot_group, resp=True, display=False):
#     pot_array = pot_group.get_pots()
#     for pot in pot_array:
#         i2c_write_data(pot.I2C_set_command(), resp, display)

def save_transient(trans_resp,file_name,trial_num):
    sample_base = range(0,len(trans_resp))
    time_base = [float(x)/float(sampleFreq) for x in sample_base]
    trans_data = np.array([sample_base,time_base,trans_resp]).T
    trial = "%04d" % (trial_num)
    np.savetxt("%s_%s.%s" % (file_name,trial,ext), trans_data, delimiter=',', fmt='%.6f')

def r_par_eq(R1,R2):
    a = float(R1)
    b = float(R2)
    if a*b == 0:
        return 0
    else:
        return a*b/(a+b)

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
    current.setCurrentDC("10mA", "MAX")
    current.setTriggerSource()
    current.setTriggerCount(totalSamples)
    current.setInitiate()

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

    # Initalize Potentiometers for Test
    i2c_group_write_data(RG2.set_pos_to_min())
    i2c_group_write_data(RG1.set_pos_to_min())

    time.sleep(0.1)

    ''' Experiment Code '''
    print "Loop Through Pot Values"
    first_loop = True
    for ii in RG2.iterator():

        # clear DMM measurements
        voltage.getMeasurements()
        current.getMeasurements()

        # send new positions to pots
        i2c_group_write_data(RG2,display=False)

        # wait for transient response
        # time.sleep(0.0005)

        # record DMM voltages as transient response
        trans_resp_volt = voltage.getMeasurements()
        steady_state_volt = np.mean(trans_resp_volt[-5:])

        trans_resp_curr = current.getMeasurements()
        steady_state_curr = np.mean(trans_resp_curr[-5:])

        # save transient response into file
        # save_transient(trans_resp_volt,'current_src_v2_c2_volt_trans',ii)
        # save_transient(trans_resp_curr,'current_src_v2_c2_curr_trans',ii)
        #save_transient(trans_resp_curr*trans_resp_volt,'current_src_v2_c2_power_trans',ii)

        # record steady state into array
        r_tmp = [ii, RG1.get_ideal_value(), RG2.get_ideal_value(), steady_state_curr, steady_state_volt]
        print r_tmp

        if first_loop:
            steady_data = np.array([r_tmp])
            first_loop = False
        else:
            steady_data = np.append(steady_data,[r_tmp], 0)

        # increment RG2
        RG2.increment()
        ii += 1
        ''' End Experimentation While Loop '''

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


