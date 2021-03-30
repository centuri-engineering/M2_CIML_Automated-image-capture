""" Scanner class definition """
# libraries import
import os
import time
from functools import partial 

import serial

import RPi.GPIO as GPIO
from picamera import PiCamera


from functions import (
    well_scan,
    box_scan,
    homing,
    simple_line,
    serial_com_check,
    scan
)

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

    def scan_photo(self, camera=None, preview=True):
        """ Scan with taking pictures"""
        if camera is None:
            camera = PiCamera(resolution=(2592, 1952))  # resolution=(4056, 3040)

        try:
            camera.hflip = True
            camera.shutter_speed = 30000  # to avoid blinking
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
                    action=partial(self.capture, camera=camera),
                    img_dir=self.conf.img_dir
                )
                GPIO.cleanup()
            if preview:
                camera.stop_preview()
        except KeyboardInterrupt:
            print("Scan interrupted by typing ctrl+c on the keybpad.")
        finally:
            GPIO.cleanup()

    def capture(self, im_path=None, camera=None):
        
        timestr = time.strftime("%Y%m%d_%H%M%S")
        if im_path is None:
            im_path = self.conf.img_dir / f"cap_{timestr}.png"

        if camera is None:
            res_buf = None
            camera = PiCamera(resolution=(2592, 1952))  # resolution=(4056, 3040)
        else:
            res_buf = camera.resolution
            camera.resolution = (2592, 1952)
            
        with open(im_path, 'bw') as fh:
            camera.capture(fh)
        if res_buf:
            camera.resolution = res_buf
        print(f"captured {im_path}")
