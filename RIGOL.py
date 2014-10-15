import socket
import time
import struct

class RIGOL:
    PORT = 5555

    def __init__(self, host, port=PORT):
        self.host = host
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((host, port))

	self.f = self.s.makefile("rb")

        #RESET
        self.s.send("*RST\n")

        #set output load
        self.s.send("OUTP:STAT OFF")

    def setOutput(self, status):
        if status:
            #enable the output
            self.s.send("OUTPut:STATe ON\n")
        else:
            self.s.send("OUTPut:STATe OFF\n")

    def getCurrent(self):
        self.s.send("MEASure:CURRent?\n")
        c = self.s.recv(1)
        if c != "#":
            print "*%s*"%(c,)
            return ""

    def getID(self):
        self.s.send("*IDN?\n")
        c = self.s.recv(1)
        print c

if __name__ == "__main__":
    r = RIGOL("192.168.2.4")
    #r.setOutput(1)
    while(1):
        #r.getCurrent()
        r.getID()
