#!/bin/bash

set -e

SCRIPT_DIR=$(cd $(dirname $0); pwd)
PROJECT_ROOT=$(cd $SCRIPT_DIR/..; pwd)
cd $PROJECT_ROOT

mkdir -p $PROJECT_ROOT/output/jpg/
DATETIME=$(date '+%Y%m%d_%H%M%S')

# https://www.raspberrypi.com/documentation/computers/camera_software.html#rpicam-vid
# 解像度: 1920 x 1080 (FHD)
# フレームレート: 30fps
# ビットレート: 5Mbps
# コーデック: h.264
rpicam-vid \
  --hdr \
  --codec h264 \
  --width 1920 \
  --height 1080 \
  --framerate 30 \
  --timeout 10000 \
  --bitrate 5000000 \
  --flicker-period 10000 \
  --output $PROJECT_ROOT/output/$DATETIME.h264