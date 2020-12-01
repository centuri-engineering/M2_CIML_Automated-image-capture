"""
File containing the main variables and functions.
DO NOT MODIFY
"""
import serial
import time
import numpy as np
from picamera import PiCamera
from config import *

# Time when loops will start
starting_loops = np.arange(0, info["total_duration"] + 1, info["elapse_time"])

nb_well = box["nb_well_along_X"] * box["nb_well_along_Y"]
nb_box = box_array["nb_box_along_X"] * box_array["nb_box_along_Y"]

# Function creating a zigzag pattern, and returning X and Y coordinates
def well_scanning_zigzag(box):
    dish_move = (
        box["dist_inter_well"] + box["diam_well"]
    )  # distance for a single move in X = Y
    # For Y
    Ycoord_along_Y_single = np.arange(
        0, box["nb_well_along_Y"] * dish_move, dish_move
    )  # Coordinates in Y for a single line
    Ycoord_zigzag_dish = np.reshape(
        np.transpose(np.tile(Ycoord_along_Y_single, (box["nb_well_along_X"], 1))),
        (1, nb_well),
    )  # Full coordinates in Y for 1 petri dish
    # For X
    Xcoord_along_X_single = np.arange(
        0, box["nb_well_along_X"] * dish_move, dish_move
    )  # Coordinates in X for a single line
    Xcoord_along_X_goback = np.concatenate(
        (Xcoord_along_X_single, Xcoord_along_X_single[::-1]), axis=None
    )  # To use a zig-zag pattern
    Xcoord_zigzag_dish = np.tile(Xcoord_along_X_goback, (1, (box["nb_well_along_Y"])))[
        :, 0:nb_well
    ]  # Full coordinates in X for 1 petri dish
    well_coord_zigzag = np.concatenate((Xcoord_zigzag_dish, Ycoord_zigzag_dish))
    return well_coord_zigzag


def box_scanning_zigzag(box_array):
    # Making X and Y arrays for Gcode moves, for a Petri dish
    box_move_along_X = box["size_along_X"] + box_array["dist_inter_box_X"]
    box_move_along_Y = box["size_along_Y"] + box_array["dist_inter_box_Y"]
    # For X
    Xboxcoord_along_X_single = np.arange(
        0, box_array["nb_box_along_X"] * box_move_along_X, box_move_along_X
    )  # Coordinates in X for a single line of box
    Xboxcoord_along_X_goback = np.concatenate(
        (Xboxcoord_along_X_single, Xboxcoord_along_X_single[::-1]), axis=None
    )  # To use a zig-zag pattern
    Xboxcoord_zigzag_box = np.tile(
        Xboxcoord_along_X_goback, (1, box_array["nb_box_along_Y"])
    )[
        :, 0:nb_box
    ]  # Full coordinates in X for all the boxes
    # For Y
    Yboxcoord_along_Y = np.arange(
        0, box_array["nb_box_along_Y"] * box_move_along_Y, box_move_along_Y
    )  # Coordinates in Y for a single line of box
    Yboxcoord_zigzag_box = np.reshape(
        np.transpose(np.tile(Yboxcoord_along_Y, (box_array["nb_box_along_X"], 1))),
        (1, nb_box),
    )  # Full coordinates in Y for all the boxes
    box_coord_zigzag = np.concatenate((Xboxcoord_zigzag_box, Yboxcoord_zigzag_box))
    return box_coord_zigzag


def camera_control(well_coord, nb_well, box_coord, nb_box, starting_loops):
    with serial.Serial(ser_set["board_path"], ser_set["baudrate"]) as s:
        # Wake up grbl : waiting 2 seconds is enough to wake it up. Some also use "s.write(b"\r\n\r\n")" but it is not needed.
        time.sleep(2)  # Wait for grbl to initialize
        # print(s.read_all()) # Should read "Grbl 1.1f ['$' for help]" if everything goes fine
        s.flushInput()  # Flush startup text in serial input
        # s.write(b'$H') # To activate once the end stops are installed on the stage
        s.write(b"G90 \n")
        camera = PiCamera()
        camera.start_preview()
        start = time.time()  # Starts a timer
        for it0, start_loop in enumerate(starting_loops):  # Loops to take the pictures
            if (
                it0 != 0
            ):  # This statetment is here because the timer starts before the loop
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
                        + str(well_coord[0, it2] + box_coord[1, it1]).encode()
                        + b" Y"  # Send x g-code coord block to grbl
                        + str(well_coord[0, it2] + box_coord[1, it1]).encode()
                        + b"\n"
                    )  # Send Y g-code coord block to grbl

                    camera.capture(
                        "images/image"
                        + str(it0 + 1)
                        + "_box"
                        + str(it1 + 1)
                        + "_well"
                        + str(it2 + 1)
                        + ".jpg"
                    )
                    time.sleep(cam_set["delay_for_picture"])

        camera.stop_preview()
        s.close()  # Close serial port