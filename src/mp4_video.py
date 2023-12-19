#!/usr/bin/python3
from datetime import datetime
import os
from time import sleep

from picamera2 import Picamera2, Preview
from picamera2.encoders import H264Encoder, LibavH264Encoder
from picamera2.outputs import FfmpegOutput
from libcamera import controls

project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
now = datetime.now().strftime("%Y%m%d_%H%M%S")

# Picamera2がnewされると preview_configuration, still_configuration, video_configuration の３つの組み込み設定オブジェクトが初期化される
picam2 = Picamera2()

# センサーのデバッグ
# print(picam2.sensor_modes)
# print(picam2.sensor_resolution)
# print(picam2.sensor_format)

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
picam2.preview_configuration.size = (1920, 1080)
# デバッグ
# print(picam.preview_configuration)

# ビデオ設定
picam2.video_configuration.size = (1920, 1080)
picam2.video_configuration.buffer_count = 6
# デバッグ
# print(picam.still_configuration)

# --- --- --- プレビュー --- --- ---
# プレビュー開始 (configには preview, still, video が設定可能)
picam2.start(config="preview", show_preview=True)

# --- --- --- ビデオ撮影 --- --- ---
# video_configuration を設定として参照するように切り替える
picam2.switch_mode("video")

encoder = H264Encoder(bitrate=5000000, framerate=30)
#encoder = LibavH264Encoder(bitrate=5000000, framerate=30)
output = os.path.join(project_dir, f"output/{now}.mp4")
ffmpeg_output = FfmpegOutput(output_filename=output, audio=False)
picam2.start_encoder(
    encoder=encoder,
    output=ffmpeg_output,
)
picam2.start()
sleep(15)
picam2.stop()
picam2.stop_encoder()

# --- --- --- クローズ --- --- ---
picam2.close()