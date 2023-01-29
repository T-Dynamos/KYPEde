from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
import _thread
import sys
import time
from src.custom_widgets.m3_textfield import M_CardTextField


class ReloadApp(MDApp):

    data = ""

    def build(self):
        self.Main = BoxLayout()
        return self.Main

    def on_start(self):
        _thread.start_new_thread(self.reload_thread, ())

    def reload_thread(self):
        while True:
            time.sleep(0.5)
            with open(sys.argv[1], "r") as kv_file:
                data = kv_file.read()
                if self.data != data:
                    print("Reloading")
                    Clock.schedule_once(lambda arg: self.Main.clear_widgets())
                    Clock.schedule_once(
                        lambda arg: self.Main.add_widget(Builder.load_string(data))
                    )
                    self.data = data
                    kv_file.close()
                else:
                    continue


ReloadApp().run()
