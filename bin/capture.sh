#!/bin/bash
set -e

SCRIPT_DIR=$(cd $(dirname $0); pwd)
PROJECT_ROOT=$(cd $SCRIPT_DIR/..; pwd)
cd $PROJECT_ROOT

mkdir -p $PROJECT_ROOT/output
DATETIME=$(date '+%Y%m%d_%H%M%S')

# https://www.raspberrypi.com/documentation/computers/camera_software.html#rpicam-jpeg
# 利用可能な解像度の確認: rpicam-hello --list-cameras
rpicam-jpeg \
  --hdr \
  --width 4608 \
  --height 2592 \
  --timeout 5000 \
  --metering spot \
  --autofocus-mode auto \
  --output $PROJECT_ROOT/output/$DATETIME.jpg