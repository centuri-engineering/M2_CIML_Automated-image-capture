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

fun.arg_def(conf, fun)

answer = input(
    "Check the above parameters. Do you want to continue (type 'yes'/'no') ?"
)
if answer == "yes":
    scanner = scan.Scanner(conf, fun)
    scanner.scan_photo()
elif answer == "no":
    print("Program canceled.")
else:
    print("Program canceled because you did not type correctly 'yes' or 'no' ! ")
