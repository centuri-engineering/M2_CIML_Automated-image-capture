""" Scanner class definition """
# libraries import
import serial
import RPi.GPIO as GPIO
import time
from picamera import PiCamera
import os


class Scanner:
    """Class Scanner to help scan the XY stage """

    zigzag = False
    relay_light = 16

    def __init__(self, conf, fun):
        self.conf = conf
        self.fun = fun
        self.well_coord = self.fun.well_scan(self.conf, self.zigzag)
        self.box_coord = self.fun.box_scan(self.conf, self.zigzag)
        self.serial = serial.Serial(
            conf.ser_set["board_path"], conf.ser_set["baudrate"]
        )
        self.serial.close()

    def homing(self):
        """Just homing th XY stage"""
        with self.serial as s:
            self.fun.homing(s, self.conf)

    def simple_line(self, xmove, ymove):
        """Simple line code streaming"""
        with self.serial as s:
            while len(s.readline()) == 0:
                print("Waiting for the serial communication.")
            s.write(b"$x\r\n")
            time.sleep(0.1)
            self.fun.serial_com_check(s, toprint=True)
            self.fun.simple_line(s, xmove, ymove)

    def scan(self):
        """Simple scan"""
        with self.serial as s:
            self.fun.scan(s, self.well_coord, self.box_coord, self.conf)

    def scan_photo(self):
        """ Scan with taking pictures"""
        try:
            camera = PiCamera()
            camera.start_preview(fullscreen=False, window=(100, 20, 640, 480))
            camera.shutter_speed = 30000

            if not os.path.exists("images/"):
                os.makedirs("images/")
            with self.serial as s:
                GPIO.setmode(GPIO.BOARD)
                GPIO.setup(self.relay_light, GPIO.OUT)
                GPIO.output(self.relay_light, True)
                print(camera.exposure_speed)
                self.fun.scan(
                    s,
                    self.well_coord,
                    self.box_coord,
                    self.conf,
                    self.relay_light,
                    action=camera.capture,
                )
                GPIO.cleanup()
            camera.stop_preview()
        except KeyboardInterrupt:
            print("Scan interrupted by typing ctrl+c on the keybpard.")
        finally:
            GPIO.cleanup()
