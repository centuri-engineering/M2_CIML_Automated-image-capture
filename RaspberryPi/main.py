#!/usr/bin/env python #If you have several versions of Python installed, /usr/bin/env will ensure the interpreter used is the first one on your environment's $PATH
"""
G-code streaming script for grbl and automatized camera
"""

# libraries import
import config as con
import functions as fun

# Main program:
well_coord = fun.well_scanning_zigzag(con.box)
box_coord = fun.box_scanning_zigzag(con.box_array, con.box)
fun.camera_control(
    well_coord, box_coord, con.box, con.box_array, con.ser_set, con.cam_set
)
