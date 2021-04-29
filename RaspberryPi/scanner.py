""" Scanner class definition """
# libraries import
import os
import time
from functools import partial

import serial

import RPi.GPIO as GPIO

from functions import well_scan, box_scan, homing, simple_line, serial_com_check, scan
from camera import setup_camera, capture


class Scanner:
    """Class Scanner to help scan the XY stage """

    zigzag = False
    relay_light = 16

    def __init__(self, conf):
        self.conf = conf
        self.well_coord = well_scan(self.conf, self.zigzag)
        self.box_coord = box_scan(self.conf, self.zigzag)
        self.serial = serial.Serial(
            conf.ser_set["board_path"], conf.ser_set["baudrate"]
        )
        self.serial.close()

        if not self.conf.img_dir.exists():
            os.makedirs(self.conf.img_dir)

    def homing(self):
        """Just homing th XY stage"""
        with self.serial as s:
            homing(s, self.conf)

    def simple_line(self, xmove, ymove):
        """Simple line code streaming"""
        with self.serial as s:
            while len(s.readline()) == 0:
                print("Waiting for the serial communication.")
            s.write(b"$x\r\n")
            serial_com_check(s, toprint=True)
            simple_line(s, xmove, ymove)

    def scan_simple(self):
        """Simple scan"""
        with self.serial as s:
            scan(s, self.well_coord, self.box_coord, self.conf)

    def scan_photo(self, camera=None, preview=True, event=None):
        """ Scan with taking pictures"""
        try:
            camera = setup_camera(camera)
            if preview:
                camera.start_preview(fullscreen=False, window=(100, 20, 640, 480))
            with self.serial as s:
                GPIO.setmode(GPIO.BOARD)
                GPIO.setup(self.relay_light, GPIO.OUT)
                GPIO.output(self.relay_light, True)
                scan(
                    s,
                    self.well_coord,
                    self.box_coord,
                    self.conf,
                    relay=self.relay_light,
                    action=partial(capture, camera=camera),
                    img_dir=self.conf.img_dir,
                    event=event,
                )
                GPIO.cleanup()
            if preview:
                camera.stop_preview()
        except KeyboardInterrupt:
            print("Scan interrupted by typing ctrl+c on the keypad.")
        finally:
            GPIO.cleanup()
            if preview:
                camera.stop_preview()
