"""
Kivy user interface for the worm photo booth
============================================

"""
import time

import kivy
from kivy.app import App
from kivy.properties import NumericProperty, ListProperty, BooleanProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout

from scanner import Scanner
from config import Config
import config as conf

kivy.require("1.11.1")


class ScannerWidget(BoxLayout):
    head_pos = (0, 0)
    conf = Config()
    scanner = Scanner(conf)

    @property
    def head_pos_str(self):
        return f"current position: x: {self.head_pos[0]}, y: {self.head_pos[1]}"

    @property
    def picamera(self):
        """The underlying kivy camera"""
        return self.kvcamera._camera._camera

    @property
    def kvcamera(self):
        """The camera interface in kivy"""
        return self.ids["camera"]

    def scan(self):
        if not self.kvcamera._camera.stopped:
            self.kvcamera._camera.stop()
        self.scanner.scan_photo(self.picamera, preview=False)
        print("scanning")

    def move(self, dx, dy):
        x, y = self.head_pos
        self.head_pos = x + dx, y + dy
        self.ids["pos_lbl"].text = self.head_pos_str
        print(f"moving {dx}, {dy}")
        self.scanner.simple_line(dx, dy)

    def homing(self):
        self.head_pos = 0, 0
        self.ids["pos_lbl"].text = self.head_pos_str
        print(f"homing")
        self.scanner.homing()

    def capture(self):
        if not self.kvcamera._camera.stopped:
            self.kvcamera._camera.stop()
        self.scanner.capture(camera=self.picamera)

    def preview(self):
        self.kvcamera.play = not self.kvcamera.play


class ScannerApp(App):
    def build(self):
        return ScannerWidget()


ScannerApp().run()
