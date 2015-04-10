#!/usr/bin/env python
# encoding: utf-8
"""
Created by Sean Nelson on 2009-10-14.
Copyright 2009-2013 Sean Nelson <audiohacked@gmail.com>

This file is part of pyBusPirate.

pyBusPirate is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

pyBusPirate is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with pyBusPirate.  If not, see <http://www.gnu.org/licenses/>.
"""
import sys
from pyBusPirate.BinaryMode.SPI import *

class BP_SPI:
	spi = None
			
	""" enter binary mode """
	def __init__(self, port="/dev/tty.usbserial-A7004qlY", speed=115200):
		# Open Serial Port
		self.spi = SPI(port, speed)
		
	
		print "Entering binmode: ",
		if self.spi.BBmode():
			print "OK."
		else:
			print "failed."
			sys.exit()
	
		print "Entering raw SPI mode: ",
		if self.spi.enter_SPI():
			print "OK."
		else:
			print "failed."
			sys.exit()
			
		print "Configuring SPI."
		if self.spi.cfg_pins(PinCfg.POWER | PinCfg.CS | PinCfg.AUX):
			print "Failed to set SPI peripherals."
			sys.exit()
		if self.spi.set_speed(SPISpeed._2_6MHZ):
			print "Failed to set SPI Speed."
			sys.exit()
		if self.spi.cfg_spi(SPICfg.CLK_EDGE | SPICfg.OUT_TYPE):
			print "Failed to set SPI configuration.";
			sys.exit()
		self.spi.timeout(0.2)

	def read_list_data(self, size):
		data = []
		for i in range(size+1):
			data.append(0)
		return data
	
# 	def read_SPI(self):
# 		self.spi.CS_Low()
# 		self.spi.bulk_trans(5, [0xB, 0, 0, 0, 0])
# 		self.spi.CS_High()
	
	def write_SPI(self,numBytes,data):
		self.spi.CS_Low()
		self.spi.bulk_trans(numBytes, data)
		self.spi.CS_High()
	
	
	def reset_BP(self):
		print "Reset Bus Pirate to user terminal: ",
		if self.spi.resetBP():
			print "OK."
		else:
			print "failed."
			sys.exit()
			
''' TEST PROGRAM '''
if __name__ == '__main__':
	s = BP_SPI()
	
	s.reset_BP()


