#!/usr/bin/env python #If you have several versions of Python installed, /usr/bin/env will ensure the interpreter used is the first one on your environment's $PATH
"""
G-code streaming script for grbl and automatized camera
"""

# libraries import
import serial  # https://pyserial.readthedocs.io/en/latest/pyserial.html
import time  # https://pypi.org/project/pytime/
from picamera import PiCamera
import config as con
import functions as fun

# Main program:
well_coord = fun.well_scanning_zigzag(con.box)
box_coord = fun.box_scanning_zigzag(con.box_array)
fun.camera_control(well_coord, fun.nb_well, box_coord, fun.nb_box, fun.starting_loops)
