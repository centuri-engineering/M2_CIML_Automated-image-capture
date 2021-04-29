"""
Kivy user interface for the worm photo booth
============================================

"""
import os
import time
from threading import Thread, Event
from datetime import datetime
from pathlib import Path
import logging

import numpy as np
import kivy
from kivy.app import App
from kivy.properties import NumericProperty, ListProperty, BooleanProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.camera import Camera as UixCamera
from kivy.uix.image import Image
from kivy.graphics.texture import Texture

from kivy.core.camera.camera_picamera import CameraPiCamera

from scanner import Scanner
from camera import setup_camera, capture as core_capture
from config import Config


kivy.require("1.11.1")
log = logging.getLogger(__name__)


class CoreCamera(CameraPiCamera):
    """Sub class of Kivy picamera interface

    We setup the camera manually to fix the parameters
    at startup from the configuration
    """

    def init_camera(self):
        if self._camera is not None:
            self._camera.close()
        self._camera = setup_camera(self._camera, resolution=(640, 480))
        self.fps = 1.0 / self._camera.framerate
        if not self.stopped:
            self.start

        self._texture = Texture.create(self._camera.resolution)
        self._texture.flip_vertical()
        self.dispatch("on_load")

    @property
    def resolution(self):
        return self._camera.resolution

    @resolution.setter
    def resolution(self, resolution):
        self._camera.resolution = resolution


class KvCamera(Image):

    play = BooleanProperty(False)
    resolution = ListProperty([-1, -1])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._camera = CoreCamera(stopped=True)
        self._camera.bind(on_texture=self.on_tex)

    def on_play(self, instance, value):

        if not self._camera:
            return
        if value:
            self._camera.start()
        else:
            self._camera.stop()

    def on_tex(self, camera):
        self.texture = texture = camera.texture
        self.texture_size = list(texture.size)
        self.canvas.ask_update()


class ScannerWidget(BoxLayout):
    x_pos = NumericProperty(0.0)
    y_pos = NumericProperty(0.0)

    conf = Config()
    timestr = time.strftime("%Y%m%d_%H%M%S")

    conf.img_dir = Path(conf.img_dir) / timestr
    if not conf.img_dir.is_dir():
        conf.img_dir.mkdir()
    scanner = Scanner(conf)
    interrupt = Event()

    @property
    def picamera(self):
        """The underlying kivy camera"""
        return self.kvcamera._camera._camera

    @property
    def kvcamera(self):
        """The camera interface in kivy"""
        return self.ids["camera"]

    def scan(self):

        self.stop_camera()
        # self.picamera = setup_camera(self.picamera)

        self.scan_thread = Thread(
            target=self.scanner.scan_photo,
            kwargs={"camera": self.picamera, "preview": False, "event": self.interrupt},
        )

        print("start scanning thread")
        self.scan_thread.start()

    def stop(self):
        print("stopping the thread")
        try:
            self.interrupt.set()
            self.scan_thread.join()
        except AttirbuteError:
            pass

    def stop_camera(self):
        if not self.kvcamera._camera.stopped:
            self.kvcamera._camera.stop()
            self.ids["preview"].state = "normal"
            self.kvcamera.play = False

    def move(self, dx, dy):
        self.x_pos += dx
        self.y_pos += dy
        print(f"moving {dx}, {dy}")
        self.ids["pos_lbl"].text = f"x: {self.x_pos:0.2f}, y: {self.y_pos:0.2f}"

        self.scanner.simple_line(dx, dy)

    def homing(self):
        self.x_pos = 0.0
        self.y_pos = 0.0
        print(f"homing")
        self.scanner.homing()

    def capture(self):
        self.stop_camera()
        core_capture(camera=self.picamera)

    def preview(self):
        self.kvcamera.play = not self.kvcamera.play


class ScannerApp(App):
    def build(self):
        return ScannerWidget()


ScannerApp().run()
