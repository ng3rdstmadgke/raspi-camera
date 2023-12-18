# Capture a JPEG while still running in the preview mode. When you
# capture to a file, the return value is the metadata for that image.

import json
from datetime import datetime
import os
from time import sleep

from picamera2 import Picamera2, Preview
from libcamera import controls

project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
now = datetime.now().strftime("%Y%m%d_%H%M%S")

picam2 = Picamera2()

preview_config = picam2.create_preview_configuration(main={"size": (800, 600)})
picam2.configure(preview_config)

picam2.start_preview(Preview.QTGL)
picam2.start()
picam2.set_controls({
    # Appendix C: Camera controles (https://datasheets.raspberrypi.com/camera/picamera2-manual.pdf)
    "AfMode": controls.AfModeEnum.Continuous, # continuous af
    "AeFlickerMode": controls.AeFlickerModeEnum.Manual, # manual flicker
    "AeFlickerPeriod": 10000, # 50Hz (60Hz = 8333)
})

sleep(5)

metadata = picam2.capture_file(os.path.join(project_dir, f"output/{now}.jpg"))
print(json.dumps(metadata, indent=2, ensure_ascii=False))

picam2.close()