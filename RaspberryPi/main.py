#!/usr/bin/env python #If you have several versions of Python installed, /usr/bin/env will ensure the interpreter used is the first one on your environment's $PATH
"""
G-code streaming script for grbl and automatized camera
"""

# libraries import
import serial  # https://pyserial.readthedocs.io/en/latest/pyserial.html
import time  # https://pypi.org/project/pytime/
import numpy as np  # https://numpy.org/
from picamera import PiCamera

camera = PiCamera()

from config import *
from functions import *


well_coord = well_scanning_zigzag(box)
box_coord = box_scanning_zigzag(box_array)
camera_control(well_coord, nb_well, box_coord, nb_box, starting_loops)
