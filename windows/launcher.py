import os
from shutil import which

if which("xrandr") is not None:
    # get using xrandr command
    xrandr_output = os.popen(which("xrandr")).read().split("\n")

for line in xrandr_output:
    if "*" in line:
        current_resolution = [
            int(line.split("x")[0].strip()),  # width
            int(line.split("x")[-1].split(" ")[0]),  # height
        ]

from kivy.config import Config

Config.set("graphics", "borderless", "1")
Config.set("graphics", "height", round(current_resolution[-1] / 1.8))
Config.set("graphics", "width", round(current_resolution[0] // 2.5))

from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.app import MDApp
from kivy.clock import Clock
from kivy.animation import Animation
import _thread
import sys
import time


class MainLauncher(MDApp):

    screen_height = current_resolution[-1]
    screen_width = current_resolution[0]
    upscale = 2.75
    center_value = 3.3
    launcher_open = False

    def build(self):
        Window.top = self.screen_height
        return Builder.load_file("./windows/launcher.kv")

    def handler(self):
        while True:
            with open("./windows/info_launcher.file", "r") as file:
                if file.read().split("\n")[0] == "open":
                    if self.launcher_open == False:
                        Clock.schedule_once(self.animate_open)
                        self.launcher_open = True
                else:
                    if self.launcher_open == True:
                        Clock.schedule_once(self.animate_close)
                        self.launcher_open = False
                file.close()
            time.sleep(0.1)

    def write_file(self, filename, text):
        with open(filename, "w") as file:
            file.write(text)
            file.close

    def on_start(self):
        self.write_file("./windows/info_launcher.file", "close")
        _thread.start_new_thread(self.handler, ())

    def animate_close(self, *args):
        Window.left = round(self.screen_width / self.center_value)
        Animation(top=round(self.screen_width), d=0.4, t="in_out_quart").start(Window)
        Clock.schedule_once(lambda arg: Window.hide(), 0.5)

    def animate_open(self, *args):
        Window.left = round(self.screen_width / self.center_value)
        Window.show()
        Animation(
            top=round(self.screen_height / self.upscale), d=0.4, t="in_out_quart"
        ).start(Window)


while True:
    MainLauncher().run()
