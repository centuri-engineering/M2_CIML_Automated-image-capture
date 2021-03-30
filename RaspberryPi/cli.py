"""
G-code streaming script for grbl and automatized camera
"""

import argparse
import datetime
from pathlib import Path

# libraries import
import serial
from picamera import PiCamera
import RPi.GPIO as GPIO
import scanner as scan

from config import Config
from functions import hms_to_sec


# Functions
def arg_def():
    """Adds arguments when lauching the program """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--box",
        type=int,
        choices=[6, 12],
        help="defines the number of wells for the boxes used",
    )
    parser.add_argument(
        "--delay", type=str, help="defines the delay (format hh:mm:ss) after each photo"
    )
    parser.add_argument(
        "--duration",
        type=str,
        help="defines the total duration during which photos are taken (format hh:mm:ss)",
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Defines the directory in which the images will be saved",
    )
    args = parser.parse_args()

    conf = Config()
    
    if args.delay is not None:
        delay = hms_to_sec(args.delay)
        conf.info["delay"] = delay
    if args.duration is not None:
        tot_dur = hms_to_sec(args.duration)
        conf.info["total_duration"] = tot_dur
    if args.box in [6, 12]:
        conf.num_wells = args.box
    if args.output is not None:
        conf.img_dir = Path(args.output)
        
    print("Box type (nb of wells) : " + str(conf.box["name"]))
    print(
        "Delay (d, hh:mm:ss) : " + str(datetime.timedelta(seconds=conf.info["delay"]))
    )
    print(
        "Total duration (d, hh:mm:ss) : "
        + str(datetime.timedelta(seconds=conf.info["total_duration"]))
    )
    return conf

# main code
conf = arg_def()
answer = input("Check the above parameters. Do you want to continue ([Y/n) ?")
if answer in ("y", "Y", ""):
    scanner = scan.Scanner(conf)
    scanner.scan_photo()
elif answer in ("n", "N"):
    print("Program canceled.")
else:
    print("Please answer y or n")

    
