#!/bin/bash

# 動作確認: テストパターンを表示
#gst-launch-1.0 videotestsrc ! autovideosink

# 動作確認: ラズパイカメラモジュールの映像を表示
#gst-launch-1.0 \
#  libcamerasrc auto-focus-mode=2 ! video/x-raw,width=1920,height=1080,framerate=30/1,format=I420 !\
#  videoscale ! video/x-raw,width=1280,height=720 ! \
#  clockoverlay time-format="%D %H:%M:%S" ! \
#  autovideosink
#exit

# kvsに動画を送信
#KVS_STREAM_NAME="test"
#gst-launch-1.0 \
#  libcamerasrc auto-focus-mode=2 ! video/x-raw,width=1920,height=1080,framerate=30/1,format=I420 !\
#  videoscale ! video/x-raw,width=1280,height=720 ! \
#  clockoverlay time-format="%D %H:%M:%S" ! \
#  v4l2h264enc extra-controls="controls,repeat_sequence_header=1" ! video/x-h264,level='(string)4' !\
#  h264parse ! video/x-h264,stream-format=avc,alignment=au,width=1280,height=720,framerate=30/1 !\
#  kvssink stream-name="$KVS_STREAM_NAME" access-key="$AWS_ACCESS_KEY_ID" secret-key="$AWS_SECRET_ACCESS_KEY" aws-region="$AWS_DEFAULT_REGION"
#exit 

# kvsに送信しつつ、ローカルでも表示
KVS_STREAM_NAME="test"
gst-launch-1.0 \
  libcamerasrc auto-focus-mode=2 ! video/x-raw,width=1920,height=1080,framerate=30/1,format=I420 !\
  videoscale ! video/x-raw,width=1280,height=720 ! \
  clockoverlay time-format="%D %H:%M:%S" ! \
  tee name=t ! \
  queue ! \
    autovideosink t. ! \
  queue ! \
    v4l2h264enc extra-controls="controls,repeat_sequence_header=1" ! video/x-h264,level='(string)4' !\
    h264parse ! video/x-h264,stream-format=avc,alignment=au,width=1280,height=720,framerate=30/1 !\
    kvssink stream-name="$KVS_STREAM_NAME" access-key="$AWS_ACCESS_KEY_ID" secret-key="$AWS_SECRET_ACCESS_KEY" aws-region="$AWS_DEFAULT_REGION"
exit 