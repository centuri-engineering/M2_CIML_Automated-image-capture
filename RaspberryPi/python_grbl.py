#!/usr/bin/env python #If you have several versions of Python installed, /usr/bin/env will ensure the interpreter used is the first one on your environment's $PATH
"""
Simple g-code streaming script for grbl
"""

#libraries import
import serial #https://pyserial.readthedocs.io/en/latest/pyserial.html
import time #https://pypi.org/project/pytime/
import numpy as np #https://numpy.org/
import struct
def binary(num):
    return ''.join(bin(ord(c)).replace('0b', '').rjust(8, '0') for c in struct.pack('!f', num))


# Open grbl serial port
baudrate = 115200 # since grbl 1.1 is installed, the default baudrate is set to 115200
#s = serial.Serial('/dev/ttyACM0',115200) #For the Joy-it micro-controller with the CNC shield
s = serial.Serial('/dev/ttyUSB0',baudrate) #For the microcontroller/
 
# Open g-code file
f = open('somefile.gcode','r') # 'r' : open text file for reading only
 
# Wake up grbl : waiting 2 seconds is enough wake it up. Some also use "s.write(b"\r\n\r\n")" but it is not needed.
time.sleep(2)   # Wait for grbl to initialize
print(s.read_all()) # Should read "Grbl 1.1f ['$' for help]" if everything goes fine
s.flushInput()  # Flush startup text in serial input

#Individual Petri dish information
nb_well_along_Y = 4 #when taken horizontally
nb_well_along_X = 6 # when taken horizontally
nb_well = nb_well_along_X*nb_well_along_Y
dist_inter_well = 3 # in mm
diam_well = 16.3 # in mm

#Making X and Y arrays for Gcode moves
move = dist_inter_well+diam_well # distance for a single move in X = Y
Ycoord_along_Y =  np.arange(0,nb_well_along_Y*move, move)
Ycoord_zigzag = np.reshape(np.transpose(np.tile(Ycoord_along_Y, (nb_well_along_X,1))), (1,nb_well))
print(Ycoord_zigzag)

Xcoord_along_X_single = np.arange(0,nb_well_along_X*move, move)
Xcoord_along_X_goback = np.concatenate((Xcoord_along_X_single, Xcoord_along_X_single[::-1]), axis=None) # To use a zig-zag pattern 
Xcoord_zigzag = np.tile(Xcoord_along_X_goback, (1,nb_well_along_Y)) # 
print(Xcoord_zigzag)

#Boxes information
nb_box = 4
box_along_X = 127.8 # in mm
box_along_Y = 85.5 # in mm
dist_inter_box_X = 20 # in mm
dist_inter_box_Y = dist_inter_box_X # in mm

#s.write(b'$H') # To activate once the end stops are installed on the stage
s.write(b'G90 \n')
for x in range(nb_well):
    s.write(b'G0 X' + str(Xcoord_zigzag[0,x]).encode() + b'\n') # Send g-code block to grbl
    time.sleep(1)

# Close serial port
s.close()