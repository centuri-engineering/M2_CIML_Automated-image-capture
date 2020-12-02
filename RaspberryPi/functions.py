"""
File containing the main variables and functions.
DO NOT MODIFY
"""
# LIBRARIES:
import serial
import time
import numpy as np
from picamera import PiCamera
from config import *

# VARIABLES:
# Time when loops start:
starting_loops = np.arange(0, info["total_duration"] + 1, info["elapse_time"])

nb_well = box["nb_well_along_X"] * box["nb_well_along_Y"]
nb_box = box_array["nb_box_along_X"] * box_array["nb_box_along_Y"]

# FUNCTIONS
# Function 1: creating a zigzag pattern to place the camera above each well, and returning X and Y coordinates
def well_scanning_zigzag(box):
    # Distance for a single move in X = Y:
    dish_move = box["dist_inter_well"] + box["diam_well"]
    # Y coordinates:
    Ycoord_along_Y_single = np.arange(0, box["nb_well_along_Y"] * dish_move, dish_move)
    Ycoord_zigzag_dish = np.reshape(
        np.transpose(np.tile(Ycoord_along_Y_single, (box["nb_well_along_X"], 1))),
        (1, nb_well),
    )
    # X coordinates:
    Xcoord_along_X_single = np.arange(0, box["nb_well_along_X"] * dish_move, dish_move)
    Xcoord_along_X_goback = np.concatenate(
        (Xcoord_along_X_single, Xcoord_along_X_single[::-1]), axis=None
    )
    Xcoord_zigzag_dish = np.tile(Xcoord_along_X_goback, (1, (box["nb_well_along_Y"])))[
        :, 0:nb_well
    ]
    # X and Y in a single array:
    well_coord_zigzag = np.concatenate((Xcoord_zigzag_dish, Ycoord_zigzag_dish))
    return well_coord_zigzag


# Function 2 : creating a zigzag pattern to place the camera above each 1st well of each box, and returning X and Y coordinates
def box_scanning_zigzag(box_array):
    # Distance for a single move:
    box_move_along_X = box["size_along_X"] + box_array["dist_inter_box_X"]
    box_move_along_Y = box["size_along_Y"] + box_array["dist_inter_box_Y"]
    # X coordinates:
    Xboxcoord_along_X_single = np.arange(
        0, box_array["nb_box_along_X"] * box_move_along_X, box_move_along_X
    )
    Xboxcoord_along_X_goback = np.concatenate(
        (Xboxcoord_along_X_single, Xboxcoord_along_X_single[::-1]), axis=None
    )
    Xboxcoord_zigzag_box = np.tile(
        Xboxcoord_along_X_goback, (1, box_array["nb_box_along_Y"])
    )[:, 0:nb_box]
    # Y coordinates:
    Yboxcoord_along_Y = np.arange(
        0, box_array["nb_box_along_Y"] * box_move_along_Y, box_move_along_Y
    )
    Yboxcoord_zigzag_box = np.reshape(
        np.transpose(np.tile(Yboxcoord_along_Y, (box_array["nb_box_along_X"], 1))),
        (1, nb_box),
    )
    # X and Y in a single array:
    box_coord_zigzag = np.concatenate((Xboxcoord_zigzag_box, Yboxcoord_zigzag_box))
    return box_coord_zigzag


def camera_control(well_coord, nb_well, box_coord, nb_box, starting_loops):
    # Use a control manager to open serial port:
    with serial.Serial(ser_set["board_path"], ser_set["baudrate"]) as s:
        # Wake up grbl : waiting 2 seconds is enough to wake it up. Some also use "s.write(b"\r\n\r\n")" but it is not needed.
        # Wait for grbl to initialize:
        time.sleep(2)
        # print(s.read_all()) # Should read "Grbl 1.1f ['$' for help]" if everything goes fine
        # Flush startup text in serial input:
        s.flushInput()
        # To activate once the end stops are installed on the stage:
        # s.write(b'$H')
        s.write(b"G90 \n")
        camera = PiCamera()
        camera.start_preview(fullscreen=False, window=(100, 20, 640, 480))
        start = time.time()
        for it0, start_loop in enumerate(starting_loops):
            # if it0 != 0:
            while it0 != 0 and (int(time.time()) - int(start)) != int(start_loop):
                pass
            for it1 in range(nb_box):
                for it2 in range(nb_well):
                    s.write(
                        b"G0 X"
                        + str(well_coord[0, it2] + box_coord[1, it1]).encode()
                        + b" Y"
                        + str(well_coord[0, it2] + box_coord[1, it1]).encode()
                        + b"\n"
                    )
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
        s.close()
