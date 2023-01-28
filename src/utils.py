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

linux_home = os.path.expanduser("~")
