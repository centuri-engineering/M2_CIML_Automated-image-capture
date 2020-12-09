"""
File containing the main constants to be modified.
"""

# General information, time in seconds
info = {"total_duration": 400, "elapse_time": 200, "delay_for_picture": 1}

# Information about the position of the 1 well to the homing position:
pos = {"x0": 50, "y0": 50}

# Individual Petri dish information (box), dimensions (dist, diam) in mm
box = {
    "nb_well_along_X": 6,
    "nb_well_along_Y": 4,
    "dist_inter_well": 3,
    "diam_well": 16.3,
    "size_along_X": 127.8,
    "size_along_Y": 85.5,
}

# All petri dish information (boxes), dimensions (dist, size) in mm
box_array = {
    "nb_box_along_X": 2,
    "nb_box_along_Y": 2,
    "dist_inter_box_X": 20,
    "dist_inter_box_Y": 20,
}

# Serial settings
ser_set = {
    "baudrate":
    115200,  # since grbl 1.1 installed, the default baudrate is set to 115200
    # /dev/ttyACM0 (Joy-it), /dev/ttyUSB0 (original board)
    "board_path": "/dev/ttyACM0",
}

# Camera setting
cam_set = {"delay_for_picture": 1}  # in seconds
