"""
File containing the main functions.
"""
# LIBRARIES:
import sys
import time
import datetime
from itertools import product
from pathlib import Path
import numpy as np

import RPi.GPIO as GPIO


def well_scan(con, zigzag):

    """Creates a pattern to place the camera above each well,
    and returns X and Y coordinates in an array"""

    nb_well = con.box["nb_well_along_X"] * con.box["nb_well_along_Y"]
    # Distance for a single move in X = Y:
    dish_move = con.box["dist_inter_well"] + con.box["diam_well"]
    # Y coordinates:
    Ycoord_along_Y_single = np.arange(
        0, con.box["nb_well_along_Y"] * dish_move, dish_move
    )
    Ycoord_all_dish = np.reshape(
        np.transpose(np.tile(Ycoord_along_Y_single, (con.box["nb_well_along_X"], 1))),
        (1, nb_well),
    )
    # X coordinates:
    Xcoord_along_X_single = np.arange(
        0, con.box["nb_well_along_X"] * dish_move, dish_move
    )
    # zigzag scan definition
    if zigzag == True:
        Xcoord_along_X_goback = np.concatenate(
            (Xcoord_along_X_single, Xcoord_along_X_single[::-1]), axis=None
        )
    else:
        Xcoord_along_X_goback = np.concatenate(
            (Xcoord_along_X_single, Xcoord_along_X_single), axis=None
        )
    Xcoord_all_dish = np.tile(Xcoord_along_X_goback, (1, (con.box["nb_well_along_Y"])))[
        :, 0:nb_well
    ]
    # X and Y in a single array:
    well_coord = np.concatenate((Xcoord_all_dish, Ycoord_all_dish))
    return well_coord


def box_scan(con, zigzag):

    """Creates a pattern to place the camera above each well 0 of each box,
    and returns X and Y coordinates in an array"""

    nb_box = con.box_array["nb_box_along_X"] * con.box_array["nb_box_along_Y"]
    # Distance for a single move:
    box_move_along_X = con.box["size_along_X"] + con.box_array["dist_inter_box_X"]
    box_move_along_Y = con.box["size_along_Y"] + con.box_array["dist_inter_box_Y"]
    # X coordinates:
    Yboxcoord_along_Y_single = np.arange(
        0, con.box_array["nb_box_along_Y"] * box_move_along_Y, box_move_along_Y
    )
    if zigzag == True:
        Yboxcoord_along_Y_goback = np.concatenate(
            (Yboxcoord_along_Y_single, Yboxcoord_along_Y_single[::-1]), axis=None
        )
    else:
        Yboxcoord_along_Y_goback = np.concatenate(
            (Yboxcoord_along_Y_single, Yboxcoord_along_Y_single), axis=None
        )
    Yboxcoord_all_box = np.tile(
        Yboxcoord_along_Y_goback, (1, con.box_array["nb_box_along_X"])
    )[:, 0:nb_box]
    # Y coordinates:
    Xboxcoord_along_X = np.arange(
        0, con.box_array["nb_box_along_X"] * box_move_along_X, box_move_along_X
    )
    Xboxcoord_all_box = np.reshape(
        np.transpose(np.tile(Xboxcoord_along_X, (con.box_array["nb_box_along_Y"], 1))),
        (1, nb_box),
    )
    # X and Y in a single array:
    box_coord = np.concatenate((Xboxcoord_all_box, Yboxcoord_all_box))
    return box_coord


def serial_com_check(s, toprint=True):
    """Function to read the receceived data from grbl """
    # Wait for the data to be received
    while s.in_waiting != 0:
        theline = s.readline()
        if toprint == True:
            print("- Message received - " + theline.decode("utf-8"))
        if theline == b"ALARM:1\r\n":
            GPIO.cleanup()
            sys.exit(
                print(
                    "Endstop triggered, check if there is an object on the path of the camera, then restart the program."
                )
            )


def homing(s, con):
    """Homing function to place the XY stage head at the zero position. """

    print("Waiting until serial communication is working.")
    while s.in_waiting == 0:
        pass
    else:
        serial_com_check(s, toprint=True)
        print("Serial communication working.")

    s.write(b"$h\r\n")
    print("Waiting until the homing is done.")
    while s.in_waiting == 0:
        pass
    else:
        serial_com_check(s, toprint=True)
        print("Homing done.")


def simple_line(s, xmove, ymove):
    """Send a simple GCODE line with X and Y coords to grbl"""
    s.write(b"G91 \r\n")
    serial_com_check(s, toprint=True)
    s.write(b"G0 X" + str(xmove).encode() + b" Y" + str(ymove).encode() + b"\r\n")
    serial_com_check(s, toprint=True)
    s.write(b"G90 \r\n")
    serial_com_check(s, toprint=True)


def scan(
    s,
    well_coord,
    box_coord,
    con,
    img_dir=None,
    relay=None,
    action=None,
    action_args=None,
    action_kwargs=None,
    event=None,
):
    """Simple scan of the well and box."""
    if img_dir is None:
        img_dir = Path("images")
    else:
        img_dir = Path(img_dir)

    if action_args is None:
        action_args = ()
    if action_kwargs is None:
        action_kwargs = {}

    max_rate_min = 8000
    max_rate_s = max_rate_min / 60
    max_acc = 500
    # Considering acceleration and deceleration phases (hence *2):
    time_acc = (max_rate_s / max_acc) * 2
    dist_acc = max_rate_s * time_acc

    starting_loops = np.arange(0, con.info["total_duration"] + 1, con.info["delay"])
    nb_well = con.box["nb_well_along_X"] * con.box["nb_well_along_Y"]
    nb_box = con.box_array["nb_box_along_X"] * con.box_array["nb_box_along_Y"]

    while s.in_waiting == 0:
        print("Waiting for the serial connection.", end="\r")
        time.sleep(0.001)

    serial_com_check(s, toprint=True)

    s.write(b"$h\r\n")
    while s.readline() != b"ok\r\n":
        print("Waiting until the homing is done.")
        serial_com_check(s, toprint=True)

    s.write(
        b"G0 X"
        + str(con.pos["x0"]).encode()
        + b" Y"
        + str(con.pos["y0"]).encode()
        + b"\r\n"
    )

    serial_com_check(s, toprint=True)

    straight_travel = ((con.pos["x0"] ** 2) + (con.pos["y0"] ** 2)) ** 0.5

    if straight_travel < dist_acc:
        time.sleep(time_acc + con.info["delay_for_action"])
    else:
        time.sleep(
            time_acc
            + (straight_travel - dist_acc) / max_rate_s
            + con.info["delay_for_action"]
        )

    # Set the present position to X=0, Y=0
    s.write(b"G92 Y0 X0 Z0\r\n")
    serial_com_check(s, toprint=True)

    start = round(time.time())

    for it0, start_loop in enumerate(starting_loops):
        if it0 != 0 and (int(time.time()) - int(start)) != int(start_loop):
            step_time = round(time.time())
            while (int(step_time) - int(start)) != int(start_loop):
                time_left = int(step_time) - int(start)
                time.sleep(0.01)
                step_time = round(time.time())
                time_left_loop = str(
                    datetime.timedelta(seconds=(int(start_loop) - time_left))
                )
                time_left_total = str(
                    datetime.timedelta(seconds=(int(starting_loops[-1]) - time_left))
                )
                print(
                    "Time left until next loop : "
                    + time_left_loop
                    + ". Time left until the end : "
                    + time_left_total,
                    end=".\r",
                )
        if relay is not None:
            GPIO.output(relay, False)

        prev_x_mv = 0
        prev_y_mv = 0

        for it1, it2 in product(range(nb_box), range(con.info["box_loop"])):
            for it3, it4 in product(range(nb_well), range(con.info["well_loop"])):
                x_mv = str(well_coord[0, it3] + box_coord[0, it1]).encode()
                y_mv = str(well_coord[1, it3] + box_coord[1, it1]).encode()
                new_pos = b"G0 X" + x_mv + b" Y" + y_mv + b"\r\n"
                s.write(new_pos)
                print("- Message sent - " + new_pos.decode("utf-8"))
                serial_com_check(s, toprint=True)

                straight_travel = (
                    ((float(x_mv) - float(prev_x_mv)) ** 2)
                    + ((float(y_mv) - float(prev_y_mv)) ** 2)
                ) ** 0.5
                if straight_travel < dist_acc:
                    time.sleep(time_acc + con.info["delay_for_action"])
                else:
                    time.sleep(
                        time_acc
                        + (straight_travel - dist_acc) / max_rate_s
                        + con.info["delay_for_action"]
                    )
                prev_x_mv = x_mv
                prev_y_mv = y_mv
                if action is not None:
                    im_path = (
                        img_dir
                        / f"image{it0+1:04d}_box{it1+1:04d}-loop{it2+1:04d}_well{it3+1:04d}-loop{it4+1:04d}.jpg"
                    )
                    action(im_path, *action_args, **action_kwargs)
                if event and event.is_set():
                    break
            if event and event.is_set():
                break

        if relay is not None:
            GPIO.output(relay, True)

        if event and event.is_set():
            return 1


def hms_to_sec(t):
    """Displays hh:mm:ss format to seconds """
    h, m, s = [int(i) for i in t.split(":")]
    return 3600 * h + 60 * m + s
