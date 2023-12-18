#!/usr/bin/python3
from datetime import datetime
import os
from time import sleep

from picamera2 import Picamera2
from picamera2.encoders import H264Encoder, Quality
from picamera2.outputs import FfmpegOutput
from libcamera import controls

project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
now = datetime.now().strftime("%Y%m%d_%H%M%S")

picam2 = Picamera2()
video_config = picam2.create_video_configuration(buffer_count=6)
picam2.configure(video_config)

output = FfmpegOutput(output_filename=os.path.join(project_dir, f"output/{now}.mp4"), audio=False)
picam2.start_encoder(
    encoder=H264Encoder(),
    output=output,
    quality=Quality.MEDIUM,
)
picam2.start(show_preview=True)

picam2.set_controls({
    # Appendix C: Camera controles (https://datasheets.raspberrypi.com/camera/picamera2-manual.pdf)
    "AfMode": controls.AfModeEnum.Continuous, # continuous af
    "AeFlickerMode": controls.AeFlickerModeEnum.Manual, # manual flicker
    "AeFlickerPeriod": 10000, # 50Hz (60Hz = 8333)
})
sleep(15)
picam2.stop()
picam2.stop_encoder()