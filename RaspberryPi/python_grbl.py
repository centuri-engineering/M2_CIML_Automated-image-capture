#!/usr/bin/env python #If you have several versions of Python installed, /usr/bin/env will ensure the interpreter used is the first one on your environment's $PATH
"""
Simple g-code streaming script for grbl
"""

#libraries import
import serial #https://pyserial.readthedocs.io/en/latest/pyserial.html
import time #https://pypi.org/project/pytime/

# Open grbl serial port
baudrate = 115200 # since grbl 1.1 is installed, the default baudrate is set to 115200
#s = serial.Serial('/dev/ttyACM0',115200) #For the Joy-it micro-controller with the CNC shield
s = serial.Serial('/dev/ttyUSB0',baudrate) #For the microcontroller/
 
# Open g-code file
f = open('somefile.gcode','r') # 'r' : open text file for reading only
 
# Wake up grbl
#s.write(b"\r\n\r\n")
print(s.read_all())
time.sleep(2)   # Wait for grbl to initialize
print(s.read_all())
s.flushInput()  # Flush startup text in serial input
print(s.read_all())
time.sleep(2)   # Wait for grbl to initialize
print(s.read_all())
s.write(b"\r\n\r\n")
time.sleep(2)   # Wait for grbl to initialize
print(s.read_all())

print('here1')
# Stream g-code to grbl
for line in f:
    print('here2')
    l = line.strip() # Strip all EOL characters for streaming
    print('here2')
    print('Sending: ' + l, end=" ")    
    print('here2')
    s.write(l.encode() + b'\n') # Send g-code block to grbl
    print('here2')
    #grbl_out = s.readline() # Wait for grbl response with carriage return
    print('here2')
    #print (' : ' + grbl_out.strip())
    print('here2')
    time.sleep(2)   # Wait for grbl to initialize

print('here3')
# Wait here until grbl is finished to close serial port and file.
#raw_input("  Press <Enter> to exit and disable grbl.")
 
# Close file and serial port
f.close()
s.close()