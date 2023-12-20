# Picamera2 Document:
#   GitHub: https://github.com/raspberrypi/picamera2
#   PDF: https://datasheets.raspberrypi.com/camera/picamera2-manual.pdf

import json
from picamera2 import Picamera2, Preview
from libcamera import controls
from time import sleep

picam2 = Picamera2()
picam2.preview_configuration.size = (1920, 1080)

picam2.start("preview", show_preview=True)
picam2.set_controls({
    # NOTE: AF関連の設定値は今のところ動いていないっぽい
    "AfMode": controls.AfModeEnum.Continuous,
    "AfSpeed": controls.AfSpeedEnum.Fast,
    # フリッカー低減モード
    "AeFlickerMode": controls.AeFlickerModeEnum.Manual, # manual flicker
    "AeFlickerPeriod": 10000, # 50Hz=10000, 60Hz=8333
    # 測光モード
    "AeMeteringMode": controls.AeMeteringModeEnum.Spot, # CenterWeighted, Matrix, Spot
    # オートホワイトバランス
    "AwbEnable": True, # True or False
    "AwbMode": controls.AwbModeEnum.Indoor # Auto, Indoor, Daylight, Cloudy
})
#print(json.dumps(picam2.camera_controls, indent=2))
sleep(1000)
