# Picamera2 Document:
#   GitHub: https://github.com/raspberrypi/picamera2
#   PDF: https://datasheets.raspberrypi.com/camera/picamera2-manual.pdf

from datetime import datetime
import os
from time import sleep

from picamera2 import Picamera2, Preview
from picamera2.encoders import H264Encoder, Quality
from libcamera import controls

project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
now = datetime.now().strftime("%Y%m%d_%H%M%S")

# Picamera2がnewされると preview_configuration, still_configuration, video_configuration の３つの組み込み設定オブジェクトが初期化される
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
    main={"size":(1920, 1080)},
    buffer_count=4,
    controls=camera_controls,
)
picam2.configure(preview_config)
# NOTE: この時点ではまだプレビューは表示されない
picam2.start_preview(preview=Preview.QTGL)

# --- --- --- ビデオ撮影 --- --- ---
# NOTE: create_*_configurationは色々と状態を変更しているので使う直前に呼び出す
#       https://github.com/raspberrypi/picamera2/blob/main/picamera2/picamera2.py#L736
video_config = picam2.create_video_configuration(
    # 4.3. Configuration objects: https://datasheets.raspberrypi.com/camera/picamera2-manual.pdf
    main={"size":(1920, 1080)},
    buffer_count=6,
    controls=camera_controls,
)
encoder = H264Encoder(bitrate=5000000, framerate=30)
output = os.path.join(project_dir, f"output/{now}.h264")
picam2.start_recording(
    encoder=encoder,
    output=output,
    config=video_config,
)
sleep(15)
picam2.stop_recording()

# --- --- --- クローズ --- --- ---
picam2.close()