#!/bin/bash

# https://www.raspberrypi.com/documentation/computers/camera_software.html#rpicam-hello

# --metering center, spot, average, custom
rpicam-hello \
  --hdr \
  --width 1920 \
  --height 1080 \
  --framerate 30 \
  --timeout 0 \
  --metering spot \
  --autofocus-mode continuous \
  --flicker-period 10000 \