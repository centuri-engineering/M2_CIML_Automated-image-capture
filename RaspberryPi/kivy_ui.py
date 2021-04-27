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
    x_pos = NumericProperty(0.0)
    y_pos = NumericProperty(0.0)

    conf = Config()
    scanner = Scanner(conf)

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

        self.scanner.scan_photo(self.picamera, preview=False)
        print("scanning")

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
        self.scanner.capture(camera=self.picamera)

    def preview(self):
        self.kvcamera.play = not self.kvcamera.play


class ScannerApp(App):
    def build(self):
        return ScannerWidget()


ScannerApp().run()
