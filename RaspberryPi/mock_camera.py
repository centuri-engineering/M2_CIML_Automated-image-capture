import numpy as np


class PiCamera:
    def __init__(self, resolution=(400, 600)):

        self.hflip = True
        self.shutter_speed = 100
        self.resolution = resolution

    def start_preview(self, *args, **kwargs):
        print("started preview")
        return Preview

    def stop_preview(self):
        print("stoped preview")

    def capture(self, fname):
        print("capture")

    def add_overlay(self, *args, **kwargs):
        print("add overlay")
        return Overlay()


class Overlay:

    fullscreen = False
    window = (1000, 200, 480, 640)
    layer = 3
    alpha = 0


class Preview:

    fullscreen = False
    window = (1000, 200, 480, 640)
    layer = 3
    alpha = 255
    hflip = False
