"""
Application built from a  .kv file
==================================

This shows how to implicitly use a .kv file for your application. You
should see a full screen button labelled "Hello from test.kv".

After Kivy instantiates a subclass of App, it implicitly searches for a .kv
file. The file test.kv is selected because the name of the subclass of App is
TestApp, which implies that kivy should try to load "test.kv". That file
contains a root Widget.
"""
import time

import kivy
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout

kivy.require("1.11.1")


class CameraClick(BoxLayout):
    def capture(self):
        """
        Function to capture the images and give them the names
        according to their captured time and date.
        """
        camera = self.ids["camera"]
        timestr = time.strftime("%Y%m%d_%H%M%S")
        camera.export_to_png("IMG_{}.png".format(timestr))
        print("Captured")


class ScannerWidget(BoxLayout):
    # def __init__(self, head_pos=(0, 0)):
    #     self.head_pos = head_pos
    head_pos = (0, 0)

    @property
    def head_pos_str(self):
        return f"current position: x: {self.head_pos[0]}, y: {self.head_pos[1]}"

    def scan(self):
        print("scanning")

    def move(self, dx, dy):
        x, y = self.head_pos
        self.head_pos = x + dx, y + dy
        self.ids["pos_lbl"].text = self.head_pos_str
        print(f"moving {dx}, {dy}")

    def homing(self):
        self.head_pos = 0, 0
        self.ids["pos_lbl"].text = self.head_pos_str
        print(f"homing")


class ScannerApp(App):
    def build(self):
        return ScannerWidget()


ScannerApp().run()
