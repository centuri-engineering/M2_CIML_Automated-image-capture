"""
File containing the main constants to be modified.
"""

# General information, time in seconds
info = {"total_duration": 240, "elapse_time": 120, "delay_for_picture": 1}


# Individual Petri dish information (box), dimensions (dist, diam) in mm
box = {
    "nb_wells_along_X": 4,
    "nb_wells_along_y": 6,
    "dist_inter_well": 3,
    "diam_well": 16.3,
    "size_along_X": 127.8,
    "size_along_Y": 85.5,
}

# All petri dish information (boxes), dimensions (dist, size) in mm
box_grid = {
    "nb_boxes_along_X": 2,
    "nb_boxes_along_y": 2,
    "dist_inter_box_X": 20,
    "dist_inter_box_Y": 20,
}

# Camera setting
