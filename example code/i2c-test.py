#!/usr/bin/env python
# encoding: utf-8
"""
Created by Peter Huewe on 2009-10-26.
Copyright 2009 Peter Huewe <peterhuewe@gmx.de>
Based on the spi testscript from Sean Nelson

This file is part of pyBusPirate.

pyBusPirate is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

pyBusPirate is distributed in the hope that it will be useful,
;but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with pyBusPirate.  If not, see <http://www.gnu.org/licenses/>.
"""
import sys
from I2C import *
""" enter binary mode """

def i2caddr(addr, write=True):
    "convert standard address to 7 bit i2c address"
    if write:
        return ((addr << 1))
    else:
        return ((addr << 1) + 1)

def i2c_scan(data):
    error = 0
    addr = data[0]
    i2c.send_start_bit()
    for i in data:
        status = i2c.bulk_trans(1, [i])
        if status.find(chr(0x01)) != -1:
            error = 1
    i2c.send_stop_bit()
    return error

def i2c_write_data(data, resp=True):
    error = 0
    addr = data[0]
    i2c.send_start_bit()
    for i in data:
        status = i2c.bulk_trans(1, [i])
        if(resp):
            if status.find(chr(0x01)) != -1:
                print chr(i) + " NACK"
                error = 1
    i2c.send_stop_bit()
    if error:
        print "I2C command not acknowledged!"
        print [hex(x) for x in data]
        print "Reset Bus Pirate to user terminal: "
        if i2c.resetBP():
            print "OK."
        else:
            print "failed."
        sys.exit()


def i2c_read_bytes(address, numbytes, ret=False):
    data_out=[]
    i2c.send_start_bit()
    i2c.bulk_trans(len(address),address)
    while numbytes > 0:
        if not ret:
            print hex(ord(i2c.read_byte()))
        else:
            data_out.append(hex(ord(i2c.read_byte())))
        if numbytes > 1:
            i2c.send_ack()
        numbytes-=1
    i2c.send_nack()
    i2c.send_stop_bit()
    if ret:
        return data_out

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "usage: %s <address> <port>"%sys.argv[0]
        sys.exit(1)

    address = int(sys.argv[1], 0)

    if len(sys.argv) == 3:
        i2c = I2C(sys.argv[2], 115200)
    else:
        i2c = I2C("/dev/tty.usbserial-A4013E5K", 115200)

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
        #if not i2c.cfg_pins(I2CPins.PULLUPS):
        print "Failed to set I2C peripherals."
        sys.exit()
    if not i2c.set_speed(I2CSpeed._400KHZ):
        print "Failed to set I2C Speed."
        sys.exit()
    i2c.timeout(0.2)

        #while(1):
    print "Toggle RED"
    i2c_write_data([i2caddr(address), 0x52, 0x45, 0x44])
    print "Toggle GREEN"
    i2c_write_data([i2caddr(address), 0x47, 0x52, 0x45, 0x45, 0x4e])
    print "Toggle BLUE"
    i2c_write_data([i2caddr(address), 0x42, 0x4c, 0x55, 0x45])
    print "LED OFF"
    i2c_write_data([i2caddr(address), 0x4c, 0x45, 0x44, 0x20, 0x4f, 0x46, 0x46])

    index = 0x01;
    count = 0
    
    while (index < 0x80):
        print "Toggle RED @ " + ("%02x" % ord(chr(index)))
        resp = i2c_scan([i2caddr(index), 0x52, 0x45, 0x44])
        if resp != 0x01:
            resp = i2c_scan([i2caddr(index), 0x4c, 0x45, 0x44, 0x20, 0x4f, 0x46, 0x46])
        if resp:
            print "No responds!"
        else:
            count = count + 1
        index = index + 1
    
    print "Total %03d" % count
    
    """
    print "Run BSL"
    i2c_write_data([i2caddr(address), 0x52, 0x55, 0x4e, 0x20, 0x42, 0x53, 0x4c])
    print "Mass Erase"
    i2c_write_data([i2caddr(address), 0x80, 0x01, 0x00, 0x15, 0x64, 0xa3])
    print "RX BSL Password"
    i2c_write_data([i2caddr(address), 0x80, 0x21, 0x00, 0x11] + ([0xFF] * 32)
    + [0x9e, 0xe6])
    print i2c_read_bytes([i2caddr(address, False)], 8, True)
    print "TX BSL Version"
    i2c_write_data([i2caddr(address), 0x80, 0x01, 0x00, 0x19, 0xe8, 0x62])
    print i2c_read_bytes([i2caddr(address, False)], 11, True)
    """
    print "Reset Bus Pirate to user terminal: "
    if i2c.resetBP():
        print "OK."
    else:
        print "failed."
    sys.exit()

