# Picamera2 Document:
#   GitHub: https://github.com/raspberrypi/picamera2
#   PDF: https://datasheets.raspberrypi.com/camera/picamera2-manual.pdf

from picamera2 import Picamera2, Preview
from libcamera import controls
from time import sleep

picam2 = Picamera2()

picam2.set_controls({
    # NOTE: AF関連の設定値は今のところ動いていないっぽい
    "AfMode": controls.AfModeEnum.Continuous,
    "AfRange": controls.AfRangeEnum.Full,
    "AfSpeed": controls.AfSpeedEnum.Fast,
    #"AfMetering": controls.AfMeteringEnum.Windows,
    #"AfWindows": [(0.25, 0.25, 0.5, 0.5)],
})
picam2.preview_configuration.size = (1920, 1080)

picam2.start("preview", show_preview=True)
sleep(1000)
