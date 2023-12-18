#!/usr/bin/python3

from datetime import datetime
import os
# picamera2: https://github.com/raspberrypi/picamera2
# documentation
from picamera2 import Picamera2

project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


picam2 = Picamera2()
now = datetime.now().strftime("%Y%m%d_%H%M%S")
picam2.start_and_record_video(
    output=os.path.join(project_dir, f"output/{now}.mp4"),
    duration=10,
)