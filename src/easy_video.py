from datetime import datetime
import os
from picamera2 import Picamera2
from libcamera import controls
from picamera2.encoders import Quality

project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
now = datetime.now().strftime("%Y%m%d_%H%M%S")

# picamera2: https://github.com/raspberrypi/picamera2
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

# --- --- --- ビデオ撮影 --- --- ---
# start_and_record_video: https://github.com/raspberrypi/picamera2/blob/main/picamera2/picamera2.py#L1851
video_config = picam2.create_video_configuration(
    main={"size":(1920, 1080)},
    controls=camera_controls,
)
picam2.start_and_record_video(
    output=os.path.join(project_dir, f"output/{now}.mp4"),
    duration=10,
    config=video_config,
    quality=Quality.HIGH,
    show_preview=True,
)