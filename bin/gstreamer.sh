#!/bin/bash

# テスト
# GStreamerの使い方 - 入門編: https://zenn.dev/hidenori3/articles/541cc59c0106b7
#gst-launch-1.0 videotestsrc ! autovideosink

# カメラの映像をデスクトップに表示する
# Install GStreamer 1.18 on Raspberry Pi 4.: https://qengineering.eu/install-gstreamer-1.18-on-raspberry-pi-4.html
#gst-launch-1.0 libcamerasrc ! \
#  video/x-raw, width=1920, height=1080, framerate=30/1 ! \
#  videoconvert ! \
#  videoscale ! \
#  clockoverlay time-format="%D %H:%M:%S" ! \
#  autovideosink
#
#exit

# カメラの映像をKVSに送信する
# kvssinkのインストール
#   - https://github.com/awslabs/amazon-kinesis-video-streams-producer-sdk-cpp
# awslabs/amazon-kinesis-video-streams-producer-sdk-cpp | GitHub:
#   - How to run sample applications for sending media to KVS using GStreamer:
#     https://github.com/awslabs/amazon-kinesis-video-streams-producer-sdk-cpp/blob/master/docs/raspberry-pi.md#how-to-run-sample-applications-for-sending-media-to-kvs-using-gstreamer
# GStreamer の起動コマンドの例 | AWS:
#   https://docs.aws.amazon.com/ja_jp/kinesisvideostreams/latest/dg/examples-gstreamer-plugin.html#examples-gstreamer-plugin-launch
# kvssinkのパラメータ
#   https://docs.aws.amazon.com/ja_jp/kinesisvideostreams/latest/dg/examples-gstreamer-plugin-parameters.html

KVS_STREAM_NAME="test"
gst-launch-1.0 libcamerasrc auto-focus-mode=on ! \
  video/x-raw,width=1920,height=1080,framerate=30/1,format=I420 !\
  videoconvert !\
  videoscale ! \
  clockoverlay time-format="%D %H:%M:%S" ! \
  v4l2h264enc extra-controls="controls,repeat_sequence_header=1" !\
  video/x-h264,level='(string)4' !\
  h264parse !\
  video/x-h264,stream-format=avc, alignment=au,width=1920,height=1080,framerate=30/1 !\
  kvssink stream-name="$KVS_STREAM_NAME" access-key="$AWS_ACCESS_KEY_ID" secret-key="$AWS_SECRET_ACCESS_KEY" aws-region="$AWS_DEFAULT_REGION"
