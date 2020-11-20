#!/usr/bin/env python
"""\
Simple g-code streaming script for grbl
"""
 
import serial
import time
 
# Open grbl serial port
#s = serial.Serial('/dev/ttyACM0',115200)
s = serial.Serial('/dev/ttyUSB0',115200)

 
# Open g-code file
f = open('somefile.gcode','r')
 
# Wake up grbl
s.write(b"\r\n\r\n")
time.sleep(2)   # Wait for grbl to initialize
s.flushInput()  # Flush startup text in serial input
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