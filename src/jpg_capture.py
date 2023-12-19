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

# Picamera2がnewされると preview_configuration, still_configuration, video_configuration の３つの組み込み設定オブジェクトが初期化される
picam2 = Picamera2()

# --- --- --- カメラコントロール --- --- ---
# # Appendix C: Camera controles (https://datasheets.raspberrypi.com/camera/picamera2-manual.pdf)
picam2.set_controls({
    # オートフォーカスモード
    "AfMode": controls.AfModeEnum.Auto, # Auto, Continuous, Manual
    # マルチパターン測光?
    "AeMeteringMode": controls.AeMeteringModeEnum.Matrix, # CenterWeighted, Matrix, Spot
    # フリッカー低減モード
    "AeFlickerMode": controls.AeFlickerModeEnum.Manual, # manual flicker
    "AeFlickerPeriod": 10000, # 50Hz=10000, 60Hz=8333
    # RaspberryPiカメラモジュール3のハードウェアHDRについて
    # Picamera2では、ハードウェアHDR機能をサポートしていないため、有効・無効の切り替えは外部コマンドで行う
    #   - 有効化: v4l2-ctl --set-ctrl wide_dynamic_range=1 -d /dev/v4l-subdev0
    #   - 無効化: v4l2-ctl --set-ctrl wide_dynamic_range=0 -d /dev/v4l-subdev0
    # ちなみにソフトウェア HDR の機能は存在するが、ほぼほぼラズパイ5にならないと使えない
})
# デバッグ
# print(json.dumps(picam.camera_controls, indent=2))

# --- --- --- 設定 --- --- ---
# 4.3. Configuration objects: (https://datasheets.raspberrypi.com/camera/picamera2-manual.pdf)
# プレビュー設定
picam2.preview_configuration.size = (2304, 1296)
# デバッグ
# print(picam.preview_configuration)

# スチル設定
picam2.still_configuration.size = picam2.sensor_resolution
# デバッグ
# print(picam.still_configuration)

# --- --- --- プレビュー --- --- ---
# プレビュー開始 (configには preview, still, video が設定可能)
picam2.start(config="preview", show_preview=True)
sleep(5)

# --- --- --- スチル撮影 --- --- ---
# 設定を still に切り替える。 (ここで still_configuration を参照するようになる)
picam2.switch_mode("still")
# スチル撮影
output = os.path.join(project_dir, f"output/{now}.jpg")
res = picam2.capture_file(file_output=output)
print(json.dumps(res, indent=2, ensure_ascii=False))

# クローズ
picam2.close()