#!/usr/bin/env python
# encoding: utf-8

import os, sys, time, string, serial

def decl(items):
    "convert binary data to hex bytes for display"
    if not items:
        return "<None>"
    c = items[0]
    if isinstance(c, str) and len(c) == 1:
        ### convert chars to hex
        items = ["%03d" % ord(x) for x in items]
    elif isinstance(c, hex):
        ### convert hex to int
        items = ["%03d" % ord(x) for x in items]
    else:
        assert isinstance(c, str) and len(c) > 1
    return " ".join(items)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "usage: %s <address> <port>"%sys.argv[0]
        sys.exit(1)

    address = int(sys.argv[1], 0)

    if len(sys.argv) == 3:
        p = sys.argv[2]
    else:
        p = "/dev/tty.usbmodemfa131"

    try:
        serialport = serial.Serial(p, 115200, timeout=0.5)
    except serial.serialutil.SerialException as e:
        print e
        sys.exit()

    serialport.flushInput()
    serialport.flushOutput()

    print "Toggle LED"
    serialport.write("I \n")
    time.sleep(0.1)
    serialport.flushOutput()

    print "Toggle LED"
    serialport.write("O \n")
    time.sleep(0.1)
    serialport.flushOutput()

    print "Toggle RED"
    f = chr(address) + chr(0x52) + chr(0x45) + chr(0x44)
    serialport.write("S " + decl(f) + " \n");
    time.sleep(0.1)
    serialport.flushOutput()

    print "Toggle GREEN"
    f = chr(address) + chr(0x47) + chr(0x52) + chr(0x45) + chr(0x45) + chr(0x4e)
    serialport.write("S " + decl(f) + " \n");
    time.sleep(0.1)
    serialport.flushOutput()

    print "Toggle BLUE"
    f = chr(address) + chr(0x42) + chr(0x4c) + chr(0x55) + chr(0x45)
    serialport.write("S " + decl(f) + " \n");
    time.sleep(0.1)
    serialport.flushOutput()

    print "LED OFF"
    f = chr(address) + chr(0x4c) + chr(0x45) + chr(0x44) + chr(0x20) + chr(0x4f) + chr(0x46) + chr(0x46)
    serialport.write("S " + decl(f) + " \n");
    time.sleep(0.1)
    serialport.flushOutput()

    serialport.close()
    sys.exit()

