"""
File containing the main constants to be modified.
"""
import functions as fun

total_duration = "48:00:00"
total_duration = fun.hms_to_sec(total_duration)
delay = "00:30:00"
delay = fun.hms_to_sec(delay)

# General information, time in seconds
info = {
    "total_duration": total_duration,
    "delay": delay,
    "delay_for_action": 1,
    "well_loop": 1,
    "box_loop": 1,
}

# Information about the position of the 1 well to the homing position:
pos = {"x0": 22.6, "y0": 0.6}

# Individual Petri dish information (box), dimensions (dist, diam) in mm
# default box
box = {
    "name": "default 12 wells",
    "nb_well_along_X": 4,
    "nb_well_along_Y": 3,
    "dist_inter_well": 3.3,
    "diam_well": 22.7,
    "size_along_X": 127.8,
    "size_along_Y": 85.5,
}

box_12wells = {
    "name": "12 wells",
    "nb_well_along_X": 4,
    "nb_well_along_Y": 3,
    "dist_inter_well": 3.3,
    "diam_well": 22.7,
    "size_along_X": 127.8,
    "size_along_Y": 85.5,
}

box_6wells = {
    "name": "6 wells",
    "nb_well_along_X": 3,
    "nb_well_along_Y": 2,
    "dist_inter_well": 3.6,
    "diam_well": 35.7,
    "size_along_X": 127.8,
    "size_along_Y": 85.5,
}

# All petri dish information (boxes), dimensions (dist, size) in mm
box_array = {
    "nb_box_along_X": 2,
    "nb_box_along_Y": 2,
    "dist_inter_box_X": 26.1,
    "dist_inter_box_Y": 26.1,
}

# Serial settings
ser_set = {
    "baudrate": 115200,  # since grbl 1.1 installed, the default baudrate is set to 115200
    # /dev/ttyACM0 (Joy-it), /dev/ttyUSB0 (original board)
    "board_path": "/dev/ttyACM0",
}
