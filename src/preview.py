# Picamera2 Document:
#   GitHub: https://github.com/raspberrypi/picamera2
#   PDF: https://datasheets.raspberrypi.com/camera/picamera2-manual.pdf

import json
from picamera2 import Picamera2, Preview
from libcamera import controls
from time import sleep

picam2 = Picamera2()

# センサーのデバッグ
# print(picam2.sensor_modes)
# print(picam2.sensor_resolution)
# print(picam2.sensor_format)

# --- --- --- カメラ設定 --- --- ---
# # Appendix C: Camera controles: https://datasheets.raspberrypi.com/camera/picamera2-manual.pdf
camera_controls = {
    # AF設定
    "AfMode": controls.AfModeEnum.Continuous,
    "AfSpeed": controls.AfSpeedEnum.Fast,
    # フリッカー低減モード
    "AeFlickerMode": controls.AeFlickerModeEnum.Manual, # manual flicker
    "AeFlickerPeriod": 10000, # 50Hz=10000, 60Hz=8333
    # 測光モード
    "AeMeteringMode": controls.AeMeteringModeEnum.Matrix, # CenterWeighted, Matrix, Spot
    # オートホワイトバランス
    "AwbEnable": True, # True or False
    "AwbMode": controls.AwbModeEnum.Indoor # Auto, Indoor, Daylight, Cloudy
    # HDR
    # Picamera2では、RaspberryPiカメラモジュール3のハードウェアHDRをサポートしていないため、有効・無効の切り替えは外部コマンドで行う
    # ちなみにソフトウェアHDRの機能は存在するが、ラズパイ5にならないと使えない
    #   - 有効化: v4l2-ctl --set-ctrl wide_dynamic_range=1 -d /dev/v4l-subdev0
    #   - 無効化: v4l2-ctl --set-ctrl wide_dynamic_range=0 -d /dev/v4l-subdev0
}

# NOTE: create_*_configurationは色々と状態を変更しているので使う直前に呼び出す
#       https://github.com/raspberrypi/picamera2/blob/main/picamera2/picamera2.py#L668
preview_config = picam2.create_preview_configuration(
    # 4.3. Configuration objects: https://datasheets.raspberrypi.com/camera/picamera2-manual.pdf
    main={"size":(1920, 1080)},
    buffer_count=4,
    controls=camera_controls,
)

# NOTE: configを適用して、プレビューを起動して、カメラを起動
#       https://github.com/raspberrypi/picamera2/blob/main/picamera2/picamera2.py#L1129
picam2.start(config=preview_config, show_preview=True)

sleep(1000)

# --- --- --- クローズ --- --- ---
picam2.close()