import time
from machine import I2C

class SI7021(object):
	'Si7021-A20 sensor library for Pycom LoPy'
	
	# Definitions.
	# https://www.silabs.com/Support%20Documents%2FTechnicalDocs%2FSi7021-A20.pdf
	
	# Slave address
	ADDR = 0x40
	
	# Commands
	# HOLD = use of clock line
	HUMD_MEASURE_HOLD = 0xE5
	HUMD_MEASURE_NOHOLD = 0xF5
	TEMP_MEASURE_HOLD = 0xE3
	TEMP_MEASURE_NOHOLD = 0xF3
	TEMP_PREV = 0xE0
	
	WRITE_USER_REG = 0xE6
	READ_USER_REG = 0xE7
	SOFT_RESET = 0xFE
	
	HTRE = 0x02
	
	i2c = None
	
	def __init__(self):
		self.i2c = I2C(0, I2C.MASTER)
		
	def measure(self, command):
		# Read only msb and lsb for old temp
		nBytes = 3
		if (command == self.TEMP_PREV):
			nBytes = 2
		
		# Write command to sensor
		self.i2c.writeto(self.ADDR, bytearray([command]))
		# Wait for conversion
		time.sleep(0.5)
		
		# msb = 0
		# lsb = 1
		recv = self.i2c.readfrom(self.ADDR, 2)
		
		# Clear last bits of lsb to 00
		cleared = recv[1] & 0xFC
		measurement = recv[0] << 8 | cleared
		return measurement
		
	def writeReg(self, value):
		self.i2c.writeto(self.ADDR, bytearray([self.WRITE_USER_REG]))
		self.i2c.writeto(self.ADDR, bytearray([value]))
		
	def readReg(self):
		self.i2c.writeto(self.ADDR, bytearray([self.READ_USER_REG]))
		recv = self.i2c.readfrom(self.ADDR, 1)
		return recv
		
	def _BV(self, bit):
		return 1 << bit
	
	def getRH(self):
		code = self.measure(self.HUMD_MEASURE_HOLD)
		return ((125.0 * code / 65536) - 6)
		
	def getTemp(self):
		code = self.measure(self.TEMP_MEASURE_HOLD)
		return ((175.72 * code / 65536) - 46.85)
		
	# Read temp from previous HD measurement
	def readTemp(self):
		code = self.measure(self.TEMP_PREV)
		return ((175.72 * code / 65536) - 46.85)
		
	def heaterOn(self):
		reg_val = self.readReg()
		reg_val |= self._BV(self.HTRE)
		self.writeReg(reg_val)
		
	def heaterOff(self):
		reg_val = self.readReg()
		reg_val &= ~self._BV(self.HTRE)
		self.writeReg(reg_val)
	
	def reset(self):
		self.writeReg(SOFT_RESET)
