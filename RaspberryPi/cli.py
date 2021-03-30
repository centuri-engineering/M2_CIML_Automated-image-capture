"""
G-code streaming script for grbl and automatized camera
"""

# libraries import
import config as conf
import functions as fun
import serial
from picamera import PiCamera
import RPi.GPIO as GPIO
import scanner as scan
import argparse
import datetime

# Functions
def arg_def(conf, fun):
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
    args = parser.parse_args()
    if args.delay is not None:
        delay = fun.hms_to_sec(args.delay)
        conf.info["delay"] = delay
    if args.duration is not None:
        tot_dur = fun.hms_to_sec(args.duration)
        conf.info["total_duration"] = tot_dur
    if args.box == 6:
        conf.box = conf.box_6wells
    elif args.box == 12:
        conf.box = conf.box_12wells

    print("Box type (nb of wells) : " + str(conf.box["name"]))
    print(
        "Delay (d, hh:mm:ss) : " + str(datetime.timedelta(seconds=conf.info["delay"]))
    )
    print(
        "Total duration (d, hh:mm:ss) : "
        + str(datetime.timedelta(seconds=conf.info["total_duration"]))
    )


# main code
arg_def(conf, fun)
answer = input("Check the above parameters. Do you want to continue ([Y/n) ?")
if answer in ("y", "Y", ""):
    scanner = scan.Scanner(conf, fun)
    scanner.scan_photo()
elif answer in ("n", "N"):
    print("Program canceled.")
else:
    print("Program canceled because you did not type correctly 'y' or 'n' ! ")
