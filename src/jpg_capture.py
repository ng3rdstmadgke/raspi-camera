# Picamera2 Document:
#   GitHub: https://github.com/raspberrypi/picamera2
#   PDF: https://datasheets.raspberrypi.com/camera/picamera2-manual.pdf

import json
from datetime import datetime
import os
from time import sleep

from picamera2 import Picamera2, Preview
from libcamera import controls

project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
now = datetime.now().strftime("%Y%m%d_%H%M%S")

picam2 = Picamera2()

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


# --- --- --- プレビュー表示 --- --- ---
# NOTE: create_*_configurationは色々と状態を変更しているので使う直前に呼び出す
#       https://github.com/raspberrypi/picamera2/blob/main/picamera2/picamera2.py#L668
preview_config = picam2.create_preview_configuration(
    # 4.3. Configuration objects: https://datasheets.raspberrypi.com/camera/picamera2-manual.pdf
    main={"size": (2304, 1296)},
    buffer_count=4,
    controls=camera_controls,
)
# NOTE: configを適用して、プレビューを起動して、カメラを起動
#       https://github.com/raspberrypi/picamera2/blob/main/picamera2/picamera2.py#L1129
picam2.start(config=preview_config, show_preview=True)
sleep(15)


# --- --- --- スチル撮影 --- --- ---
# NOTE: create_*_configurationは色々と状態を変更しているので使う直前に呼び出す
#       https://github.com/raspberrypi/picamera2/blob/main/picamera2/picamera2.py#L702
still_config = picam2.create_still_configuration(
    # 4.3. Configuration objects: https://datasheets.raspberrypi.com/camera/picamera2-manual.pdf
    main={"size": picam2.sensor_resolution},
    buffer_count=1,
    controls=camera_controls,
)
# NOTE: switch_mode_and_capture_file は ざっくり stop, configure, start, capture_file をまとめたもの
#       https://github.com/raspberrypi/picamera2/blob/main/picamera2/picamera2.py#L1386
res = picam2.switch_mode_and_capture_file(
    camera_config=still_config,
    file_output=os.path.join(project_dir, f"output/{now}.jpg")
)
print(json.dumps(res, indent=2, ensure_ascii=False))


# --- --- --- クローズ --- --- ---
picam2.close()