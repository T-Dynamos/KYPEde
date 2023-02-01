import subprocess
import time
import os
from shutil import which
import json

LAUNCHER_FILE = "./src/launcher.py"
UNIVERSAL_OPTIONS = ["add", "modal"]
BOTTOMBAR_FILE = "./src/bottombar.py"
BOTTOMBAR_OPTIONS = ["add", "above", "sticky"]
SOUND_FILE = "./src/sound.py"

bottombar = subprocess.Popen([which("python3"), BOTTOMBAR_FILE])
launcher = subprocess.Popen([which("python3"), LAUNCHER_FILE])
sound = subprocess.Popen([which("python3"), SOUND_FILE])

time.sleep(6)  # time for running windows

output = subprocess.run([which("wmctrl"), "-l", "-p"], capture_output=True)

output = output.stdout.decode().strip()

for line in output.split("\n"):
    if str(bottombar.pid) in line:
        bottom_bar_windowid = line.split(" ")[0]
    elif str(launcher.pid) in line:
        launcher_bar_windowid = line.split(" ")[0]
    elif str(sound.pid) in line:
        sound_bar_windowid = line.split(" ")[0]


add_options = lambda options, window_id: os.system(
    "{} -b {} -i -r {}".format(which("wmctrl"), ",".join(options), window_id)
)

try:
    add_options(UNIVERSAL_OPTIONS, launcher_bar_windowid)
    add_options(UNIVERSAL_OPTIONS, sound_bar_windowid)
    add_options(BOTTOMBAR_OPTIONS, bottom_bar_windowid)
except Exception:
    pass

json.dump(
    {
        "bottombar": bottom_bar_windowid,
        "launcher": launcher_bar_windowid,
        "sound": sound_bar_windowid,
    },
    open("dynamic_view.json", "w"),
)

kill_pid = lambda pid: os.system("kill {}".format(pid))


while True:
    try:
        time.sleep(0.1)
    except Exception:
        kill_pid(bottombar.pid)
        kill_pid(launcher.pid)
        kill_pid(sound.pid)
        exit()
