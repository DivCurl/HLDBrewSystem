### TODO
# 1. Verify steps, equipment, and sequencer with Ben
# 2. I/O - use GPIO module on Pi or peripheral board?
# 3. 
# 4. 
# 5. 

''' 
# 1. Startup by operator
# 2. Check Equipment Status 
# 3. Set/Verify Setpoints
# 4. Prompt Operator Input (if needed)
# 5. Run Sequencers, Log Data as needed to memory
# 6. Loop 4, 5 Until All Steps Complete
# 7. Log all data to SQL
# 8. Shutdown (All Idle)
 
----------------------
MAIN PROCESS STEPS
* CIP
* Lauter Tank
* Boil Mash
* Rest
* Cool (HeatEx) & transfer to fermenter carboy
* ??? 
 
----------------------
Sequencer Steps (Generic):
Heating
Cooling
Automatic transfer (pump)
Manual transfer
Dwell for operator input/advance
Dwell for temp
Dwell for time
...?
----------------------
'''

DEBUG = True
REVISION = 0.1

import sys
import os
# import threading
import platform
import math
import datetime  # for timestamping events for SQL
import time
try: 
	import MySQLdb 
except ImportError:
	print( "MySQLdb not installed: SQL functionality disabled!" )
	skipSQL = True
try: 
	import RPi.GPIO as GPIO 
except ImportError:
	print( "RPi not installed: functionality disabled!" )
	skipPi = True
	
'''
GLOBAL FUNCTIONS
'''	
def scale ( input, inMin, inMax, outMin, outMax ):
	output = ( input - inMin ) / ( inMax - inMin ) * ( outMax - outMin ) + outMin
	return output
	
'''
GLOBAL CLASSES
'''	
# Analog Sensor
# if not assinged at instantiation, default input range = 0-100	
'''
Note: RPI needs an ADC IC or some kind of shield/board for providing analog I/O,
though a poor man's charge/discharge ADC circuit can be built using the GPIO
ref: https://www.allaboutcircuits.com/projects/building-raspberry-pi-controllers-part-5-reading-analog-data-with-an-rpi/
'''
class sensor:
	def __init__( self, name, rawLow=0, rawHigh=100, scaledLow=0, scaledHigh=100 ):
		self.name = name
		self.rLow = rawLow
		self.rHigh = rawHigh
		self.sLow = scaledLow
		self.sHigh = scaledHigh
		if DEBUG == True:
			print(self.name + " Created") #debug	

	# bind to I/O pins...rPI doesn't have on-board ADC 
	def BindIO(): 
		pass
		
	def GetScaledValue():
		return scale( rLow, rHigh, sLow, sHigh)
		
	
class valve: 
	def __init__( self, name ):
		self.name = name
		if DEBUG == True:
			print(self.name + " Created") #debug	
		
class pump:
	def __init__( self, name ):
		self.name = name
		if DEBUG == True:
			print(self.name + " Created") #debug	
		
# Storage Vessels (tank, carboy, etc)
class vessel:
	def __init__( self, name ):
		self.name = name
		self.entities = []
		if DEBUG == True:
			print( self.name + " Created" ) #debug	
		
		
	def AddEntity( self, entity ):
		# TODO: check if entity name already exists in list before adding
		self.entities.append ( entity )
	
	def DeleteEntity ( self, entityName ):
		# loop all entities and delete the one with the matching name
		# if it doesn't exist, print std out and continue
		pass
	
	def GetEntities ( self ):	# Print all owned entities
		idx = 0
		for p in self.entities: 
			print ( self.name + " Entity " + str(idx) + ": " + p.name )
			idx += 1
		print ( '\n' )

# Generic timer class for sequencing, delays, etc.	
class timer:
	def __init__( self, preset ):
		self.en = False
		self.dn = False
		self.pre = preset		# set the preset trigger
		self.accInit = 0		# initial accumulator value
		self.accNow	= 0			# accumulator on Update
	
	def Start( self ):
		self.en = True
		self.accInit = time.time()
		
	def Stop( self ):
		self.en = False
		self.dn = False
	
	def Update( self ):
		if self.dn == False:
			self.accNow = time.time() - self.accInit
			
		if self.accNow >= self.pre:
			self.dn = True
						
	def Reset( self ):
		pass
			
	
class sql():
	pass
''' MySQL FYI for later so I don't forget

db = MySQLdb.connect(host="localhost",    # localhost should work if running on the PI, other svr IP address
                     user="user",         # your username
                     passwd="password",  # your password
                     db="myDB")        # name of the data base

# Cusor object for executing SQL queries
cur = db.cursor()

cur.execute("SELECT * FROM YOUR_TABLE_NAME")

# Test loop to print results
for row in cur.fetchall():
    print row[0]

db.close()
'''

''' 
# PROGRAM START
'''
while exit != "q":	
	# print( os.name )
	# print ( platform.system() )
	print( "\n\n### H-L-D Brewing System v." + str( REVISION ) + " ###" + "\n")
	# if timer1.en == False:
	# timer1.Start()		
	# timer1.Update()
	# print( "Timer acc value:", timer1.accNow )	
	# pmp = pump("pump1") #OK
	
	# The below are just for testing
	tun = vessel( "Tun1" )
	tun.AddEntity( pump( "pump1" ) ) #OK
	tun.AddEntity( pump( "pump2" ) ) #OK
	tun.AddEntity( sensor( "Temp1" ) ) #OK
	print( '\n' )
	tun.GetEntities()	#OK
	exit = input( "Press q to exit: " )
		


