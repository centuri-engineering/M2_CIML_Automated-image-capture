#!/usr/bin/env python #If you have several versions of Python installed, /usr/bin/env will ensure the interpreter used is the first one on your environment's $PATH
"""
G-code streaming script for grbl and automatized camera
"""

# libraries import
import serial  # https://pyserial.readthedocs.io/en/latest/pyserial.html
import time  # https://pypi.org/project/pytime/
import numpy as np  # https://numpy.org/

# General information:
total_duration = 240  # duration of the experiment in seconds
elapse_time = 120  # Time in seconds
delay_for_picture = 1  # delay in seconds
starting_loops = np.arange(
    0, total_duration + 1, elapse_time
)  # Times when loops will start

# Individual Petri dish information
nb_well_along_Y = 4  # when taken horizontally
nb_well_along_X = 6  # when taken horizontally
nb_well = nb_well_along_X * nb_well_along_Y
dist_inter_well = 3  # in mm, similar in X and Y
diam_well = 16.3  # in mm

# Making X and Y arrays for Gcode moves, for a Petri dish
dish_move = dist_inter_well + diam_well  # distance for a single move in X = Y
# For Y
Ycoord_along_Y_single = np.arange(
    0, nb_well_along_Y * dish_move, dish_move
)  # Coordinates in Y for a single line
Ycoord_zigzag_dish = np.reshape(
    np.transpose(np.tile(Ycoord_along_Y_single, (nb_well_along_X, 1))), (1, nb_well)
)  # Full coordinates in Y for 1 petri dish
# For X
Xcoord_along_X_single = np.arange(
    0, nb_well_along_X * dish_move, dish_move
)  # Coordinates in X for a single line
Xcoord_along_X_goback = np.concatenate(
    (Xcoord_along_X_single, Xcoord_along_X_single[::-1]), axis=None
)  # To use a zig-zag pattern
Xcoord_zigzag_dish = np.tile(Xcoord_along_X_goback, (1, (nb_well_along_Y)))[
    :, 0:nb_well
]  # Full coordinates in X for 1 petri dish

# Boxes information (box = petri dish)
nb_box_along_X = 2  # Number of boxes on the X axis
nb_box_along_Y = 2  # Number of boxes on the Y axis
nb_box = nb_box_along_X * nb_box_along_Y  # Total number of boxes
box_along_X = 127.8  # dimensions in mm
box_along_Y = 85.5  # dimensions in mm
dist_inter_box_X = 20  # dimensions in mm
dist_inter_box_Y = dist_inter_box_X  # dimensions in mm

# Making X and Y arrays for Gcode moves, for a Petri dish
box_move_along_X = box_along_X + nb_box_along_X
box_move_along_Y = box_along_Y + nb_box_along_Y
# For X
Xboxcoord_along_X_single = np.arange(
    0, nb_box_along_X * box_move_along_X, box_move_along_X
)  # Coordinates in X for a single line of box
Xboxcoord_along_X_goback = np.concatenate(
    (Xboxcoord_along_X_single, Xboxcoord_along_X_single[::-1]), axis=None
)  # To use a zig-zag pattern
Xboxcoord_zigzag_box = np.tile(Xboxcoord_along_X_goback, (1, nb_box_along_Y))[
    :, 0:nb_box
]  # Full coordinates in X for all the boxes
# For Y
Yboxcoord_along_Y = np.arange(
    0, nb_box_along_Y * box_move_along_Y, box_move_along_Y
)  # Coordinates in Y for a single line of box
Yboxcoord_zigzag_box = np.reshape(
    np.transpose(np.tile(Yboxcoord_along_Y, (nb_box_along_X, 1))), (1, nb_box)
)  # Full coordinates in Y for all the boxes


# Open grbl serial port
baudrate = 115200  # since grbl 1.1 is installed, the default baudrate is set to 115200
# s = serial.Serial('/dev/ttyACM0',115200) #For the Joy-it micro-controller with the CNC shield
s = serial.Serial("/dev/ttyUSB0", baudrate)  # For the microcontroller/

# Wake up grbl : waiting 2 seconds is enough to wake it up. Some also use "s.write(b"\r\n\r\n")" but it is not needed.
time.sleep(2)  # Wait for grbl to initialize
# print(s.read_all()) # Should read "Grbl 1.1f ['$' for help]" if everything goes fine
s.flushInput()  # Flush startup text in serial input
# s.write(b'$H') # To activate once the end stops are installed on the stage
s.write(b"G90 \n")

start = time.time()  # Starts a timer
for it0, start_loop in enumerate(starting_loops):  # Loops to take the pictures
    if it0 != 0:  # This statetment is here because the timer starts before the loop
        while it0 != 0 and (int(time.time()) - int(start)) != int(
            start_loop
        ):  # As long as the timer has not reached the desired duration, the loop is stuck
            pass
    for it1 in range(nb_box):  # Loop to define the coordinates of each box
        for it2 in range(
            nb_well
        ):  # Loop to define the coordinates of each well of the Petri dish
            s.write(
                b"G0 X"
                + str(
                    Xboxcoord_zigzag_box[0, it1] + Xcoord_zigzag_dish[0, it2]
                ).encode()
                + b" Y"  # Send x g-code coord block to grbl
                + str(
                    Yboxcoord_zigzag_box[0, it1] + Ycoord_zigzag_dish[0, it2]
                ).encode()
                + b"\n"
            )  # Send Y g-code coord block to grbl
            time.sleep(delay_for_picture)

s.close()  # Close serial port
