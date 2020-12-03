"""
File containing the main variables and functions.
DO NOT MODIFY
"""
# LIBRARIES:
import serial
import time
import numpy as np
from picamera import PiCamera
import config as con
from itertools import product

# FUNCTIONS
# Function 1:


def well_scanning_zigzag(box=con.box):
    """Creates a zigzag pattern to place the camera above each well,
    and returns X and Y coordinates in an array"""
    nb_well = box["nb_well_along_X"] * box["nb_well_along_Y"]
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


# Function 2 :
def box_scanning_zigzag(box_array=con.box_array, box=con.box):
    """Creates a zigzag pattern to place the camera above each well 0 of each box,
    and returns X and Y coordinates in an array"""
    nb_box = box_array["nb_box_along_X"] * box_array["nb_box_along_Y"]
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


def camera_control(
    well_coord,
    box_coord,
    box=con.box,
    box_array=con.box_array,
    ser_set=con.ser_set,
    cam_set=con.cam_set,
):
    """Starts a serial communication with the Arduino board and the CNC shield,
    starts the camera and make it move above every well of every box
    with a zigzag pattern"""
    # Time when loops start:
    starting_loops = np.arange(
        0, con.info["total_duration"] + 1, con.info["elapse_time"]
    )
    nb_well = box["nb_well_along_X"] * box["nb_well_along_Y"]
    nb_box = box_array["nb_box_along_X"] * box_array["nb_box_along_Y"]
    # Use a control manager to open serial port:
    with serial.Serial(ser_set["board_path"], ser_set["baudrate"]) as s:
        # Wake up grbl : waiting 2 seconds is enough to wake it up.
        # Some also use "s.write(b"\r\n\r\n")" but it is not needed.
        # Wait for grbl to initialize:
        time.sleep(2)
        # print(s.read_all()) # Should read "Grbl 1.1f ['$' for help]"
        # if everything goes fine
        # Flush startup text in serial input:
        s.flushInput()
        # To activate once the end stops are installed on the stage:
        # s.write(b'$H')
        # if everything goes fine
        # Flush startup text in serial input:
        s.flushInput()
        # To activate once the end stops are installed on the stage:
        # s.write(b'$H')
        s.write(b"G90 \n")
        camera = PiCamera()
        camera.start_preview(fullscreen=False, window=(100, 20, 640, 480))
        start = time.time()
        for it0, start_loop in enumerate(starting_loops):
            while it0 != 0 and (int(time.time()) - int(start)) != int(start_loop):
                pass
                for it1, it2 in product(range(nb_box), range(nb_well)):
                    x_mv = str(well_coord[0, it2] + box_coord[0, it1]).encode()
                    y_mv = str(well_coord[1, it2] + box_coord[1, it1]).encode()
                    s.write(b"G0 X" + x_mv + b" Y" + y_mv + b"\n")

                    im_path = (
                        f"images/image{it0+1:04d}_box{it1+1:04d}_well{it2+1:04d}.jpg"
                    )
                    camera.capture(im_path)
                    time.sleep(cam_set["delay_for_picture"])
        camera.stop_preview()
