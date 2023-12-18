#!/bin/bash
set - e

SCRIPT_DIR=$(cd $(dirname $0); pwd)
PROJECT_ROOT=$(cd $SCRIPT_DIR/..; pwd)
cd $PROJECT_ROOT

mkdir -p $PROJECT_ROOT/output/jpg/
DATETIME=$(date '+%Y%m%d_%H%M%S')
rpicam-jpeg \
  --hdr \
  -t 10 \
  -o $PROJECT_ROOT/output/$DATETIME.jpg