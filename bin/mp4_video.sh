#!/bin/bash

set -e

SCRIPT_DIR=$(cd $(dirname $0); pwd)
PROJECT_ROOT=$(cd $SCRIPT_DIR/..; pwd)
cd $PROJECT_ROOT

mkdir -p $PROJECT_ROOT/output
DATETIME=$(date '+%Y%m%d_%H%M%S')

# https://www.raspberrypi.com/documentation/computers/camera_software.html#rpicam-vid
# 解像度: 1920 x 1080 (FHD)
# フレームレート: 30fps
# ビットレート: 5Mbps
# コーデック: h.264 (ハードウェアエンコード)
# --libav-video-codec: ffmpeg -codecs
# --libav-video-codec-opts: ffmpeg -h encoder=h264_v4l2m2m
# --libav-format: ffmpeg -formats
# --awb indoor
rpicam-vid \
  --codec libav \
  --libav-video-codec h264_v4l2m2m \
  --libav-video-codec-opts "num_output_buffers=10;num_capture_buffers=10" \
  --libav-format mp4 \
  --width 1920 \
  --height 1080 \
  --framerate 30 \
  --bitrate 5000000 \
  --timeout 10000 \
  --flicker-period 10000 \
  --metering spot \
  --autofocus-mode continuous \
  --output $PROJECT_ROOT/output/$DATETIME.mp4