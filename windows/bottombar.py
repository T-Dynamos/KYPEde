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
Config.set("graphics", "height", round(current_resolution[-1] // 15))
Config.set("graphics", "width", round(current_resolution[0]))

from kivy.lang import Builder
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.graphics.svg import Svg
from kivy.animation import Animation
from kivy.metrics import dp, sp
from kivy.uix.anchorlayout import AnchorLayout
from kivymd.app import MDApp
from kivy.uix.anchorlayout import AnchorLayout
import _thread
import cairosvg


class DesktopIcon(AnchorLayout):
    pass


class BottomBar(MDApp):

    screen_height = current_resolution[-1]
    screen_width = current_resolution[0]
    upscale = 6.3
    launcher_open = False
    sound_open = False
    Window = Window
    user_home = "/home/" + os.popen("whoami").read()[:-1]
    bold_font = "./fonts/Poppins-Bold.ttf"
    regular_font = "./fonts/Poppins-Regular.ttf"
    medium_font = "./fonts/Poppins-Medium.ttf"
    light_font = "./fonts/Poppins-Light.ttf"
    icon_folders = ["/usr/share/icons/", f"{user_home}/.local/share/icons"]

    def build(self):
        Window.top = self.screen_height - (self.screen_height // 15)
        self.title = "BottomBar"
        Clock.schedule_once(lambda arg: Window.show(), 0.2)
        self.theme_cls.theme_style = "Light"
        return Builder.load_file("./windows/bottombar.kv")

    def on_start(self):
        loader = self.load_desktop_file("/usr/share/applications/blender.desktop")
        widget = DesktopIcon()
        widget.icon = loader[0]
        widget.run = loader[-1]
        self.root.ids.main_icon_box.add_widget(widget)

    def write_file(self, filename, text):
        with open(filename, "w") as file:
            file.write(text)
            file.close

    def open_bar(self):
        if self.launcher_open:
            self.write_file("./windows/info_launcher.file", "close")
            self.launcher_open = False
        else:
            self.write_file("./windows/info_launcher.file", "open")
            self.launcher_open = True

    def open_sound(self):
        if self.launcher_open:
            self.write_file("./windows/info_sound.file", "close")
            self.launcher_open = False
        else:
            self.write_file("./windows/info_sound.file", "open")
            self.launcher_open = True

    def get_current_icon_theme(self):
        command = os.popen("xfconf-query -c xsettings -p /Net/IconThemeName").read()
        return command.strip()

    def load_desktop_file(self, desktop_file):
        with open(desktop_file, "r") as file:
            read_file = file.read()
            for line in read_file.split("\n"):
                if line.startswith("Icon"):
                    icon = line.split("=")[-1].strip()
                elif line.startswith("Exec"):
                    run = lambda: os.system(line.split("=")[-1].strip())
            file.close()
        absolute_icon = self.locate_abs_icon(icon)
        return (self.convert_svg(absolute_icon[0], theme_icon=absolute_icon[-1]), run)

    def locate_theme_icon_path(self, theme):
        for folder in self.icon_folders:
            if os.path.isdir(folder):
                for theme_folder in os.listdir(folder):
                    if theme_folder == theme:
                        return os.path.join(folder, theme_folder)
        raise OSError("Icon theme '{}' not found".format(theme))

    def locate_abs_icon(self, icon):
        # try with current theme
        current_theme = self.get_current_icon_theme()
        for folder in os.walk(self.locate_theme_icon_path(current_theme)):
            for file in folder[-1]:
                if (
                    file.endswith(".svg")
                    and icon.strip().lower() in file.lower()
                    and (
                        "/".join(folder[0].split("/")[:-1]).endswith("apps")
                        or "/".join(folder[0].split("/")).endswith("apps")
                    )
                ):
                    return (os.path.join(folder[0], file), current_theme)

        # fallback
        fallback_theme = None
        fallback_theme_ = self.locate_supported_icon_theme(icon)
        for _f in fallback_theme_:
            if current_theme.split("-")[0] in _f:  # will detect dark icons
                fallback_theme = _f
        if fallback_theme is None:
            fallback_theme = fallback_theme_[0]  # cannot do anything here

        for fallback_folder in os.walk(fallback_theme):
            for file_fallback in fallback_folder[-1]:
                if (
                    file_fallback.endswith(".svg")
                    and icon.strip().lower() in file_fallback.lower()
                    and (
                        "/".join(fallback_folder[0].split("/")[:-1]).endswith("apps")
                        or "/".join(fallback_folder[0].split("/")).endswith("apps")
                    )
                ):
                    return (
                        os.path.join(fallback_folder[0], file_fallback),
                        fallback_theme.split("/")[-1],
                    )
        return None  # icon does not exists on system!

    def locate_supported_icon_theme(self, icon):
        supported_themes = []
        for folder_icon in self.icon_folders:
            command = os.popen(
                "find {} -name '*.svg' | grep {}".format(folder_icon, icon)
            ).read()
            for line in command.split("\n"):
                if "apps" in line:
                    for theme in self.list_all_icon_themes():
                        if theme in line:
                            supported_themes.append(theme)
                            break
        return list(set(supported_themes))

    def list_all_icon_themes(self):
        themes = []
        for folder in self.icon_folders:
            themes = themes + [
                os.path.join(folder, theme) for theme in os.listdir(folder)
            ]
        return list(set(themes))

    def convert_svg(self, filename, theme_icon=None):
        pngfile = "./tmp/{}-{}.png".format(filename.split("/")[-1][:-4], theme_icon)
        if os.path.isfile(pngfile) == False:
            cairosvg.svg2png(url=filename, write_to=pngfile)
        return pngfile


while True:
    BottomBar().run()