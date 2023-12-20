# Picamera2 Install

```bash
sudo apt-get update
sudo apt-get upgrade

# picamera2: https://pypi.org/project/picamera2/
# ※ picamera2をpipでインストールするのは非推奨らしい
sudo apt install -y python3-pyqt5 python3-opengl
sudo apt install -y python3-picamera2
```
## Documentation

- [picamera2 | GitHub](https://github.com/raspberrypi/picamera2)
  - [picamera2 manual](https://datasheets.raspberrypi.com/camera/picamera2-manual.pdf)
- [Camera software | Raspberry Pi](https://www.raspberrypi.com/documentation/computers/camera_software.html)

# Gstreamer Install

https://gstreamer.freedesktop.org/documentation/installing/on-linux.html?gi-language=c#

```bash
sudo apt-get install -y libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev libgstreamer-plugins-bad1.0-dev gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly gstreamer1.0-libav gstreamer1.0-tools gstreamer1.0-x gstreamer1.0-alsa gstreamer1.0-gl gstreamer1.0-gtk3 gstreamer1.0-qt5 gstreamer1.0-pulseaudio
```

kvssink

https://docs.aws.amazon.com/ja_jp/kinesisvideostreams/latest/dg/producer-sdk-cpp.html#producer-sdk-cpp-using

```bash
# https://github.com/awslabs/amazon-kinesis-video-streams-producer-sdk-cpp
sudo apt-get install -y cmake git pkg-config m4
cd
git clone https://github.com/awslabs/amazon-kinesis-video-streams-producer-sdk-cpp.git
mkdir -p amazon-kinesis-video-streams-producer-sdk-cpp/build
cd amazon-kinesis-video-streams-producer-sdk-cpp/build

cmake .. -DBUILD_GSTREAMER_PLUGIN=ON -DBUILD_JNI=TRUE

sudo apt-get install -y libssl-dev libcurl4-openssl-dev liblog4cplus-dev libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev gstreamer1.0-plugins-base-apps gstreamer1.0-plugins-bad gstreamer1.0-plugins-good gstreamer1.0-plugins-ugly gstreamer1.0-tools

make
```

- [Install GStreamer 1.18 on Raspberry Pi 4.](https://qengineering.eu/install-gstreamer-1.18-on-raspberry-pi-4.html)
- [libcamera Getting Started](https://libcamera.org/getting-started.html)


# Raspberry Pi で C++ プロデューサー SDK を使用する

https://docs.aws.amazon.com/ja_jp/kinesisvideostreams/latest/dg/producersdk-cpp-rpi.html

kvs C++ プロデューサーSDK インストール


```bash
# インストールの前提条件であるソフトウェアをインストールします。
# https://docs.aws.amazon.com/ja_jp/kinesisvideostreams/latest/dg/producersdk-cpp-rpi-software.html
sudo apt-get update
sudo apt-get install -y \
  automake \
  build-essential \
  cmake \
  git \
  gstreamer1.0-plugins-base-apps \
  gstreamer1.0-plugins-bad \
  gstreamer1.0-plugins-good \
  gstreamer1.0-plugins-ugly \
  gstreamer1.0-tools \
  gstreamer1.0-omx-generic \
  libcurl4-openssl-dev \
  libgstreamer1.0-dev \
  libgstreamer-plugins-base1.0-dev \
  liblog4cplus-dev \
  libssl-dev \
  pkg-config
sudo curl https://www.amazontrust.com/repository/AmazonRootCA1.pem -o /etc/ssl/AmazonRootCA1.pem
sudo chmod 644 /etc/ssl/AmazonRootCA1.pem

# Kinesis Video Streams C++ プロデューサー SDK をダウンロードしてビルド
# https://docs.aws.amazon.com/ja_jp/kinesisvideostreams/latest/dg/producersdk-cpp-rpi-download.html
git clone https://github.com/awslabs/amazon-kinesis-video-streams-producer-sdk-cpp.git
mkdir -p amazon-kinesis-video-streams-producer-sdk-cpp/build
cd amazon-kinesis-video-streams-producer-sdk-cpp/build
cmake .. -DBUILD_GSTREAMER_PLUGIN=ON -DBUILD_DEPENDENCIES=FALSE
make

# Kinesis ビデオストリームにビデオをストリーミングし、ライブストリームを視聴する
# https://docs.aws.amazon.com/ja_jp/kinesisvideostreams/latest/dg/producersdk-cpp-rpi-run.html

cat <<EOF >> ~/.bashrc

export GST_PLUGIN_PATH=${HOME}/amazon-kinesis-video-streams-producer-sdk-cpp/build
export AWS_DEFAULT_REGION=ap-northeast-1
export AWS_ACCESS_KEY_ID=xxxxxxxxxxxxxxxxxxxxxxxx
export AWS_SECRET_ACCESS_KEY=xxxxxxxxxxxxxxxxxxxxxxxx
EOF

source ~/.bashrc
```

# libcamera install

https://libcamera.org/getting-started.html

```bash
sudo apt-get install -y gstreamer1.0-libcamera gstreamer1.0-libcamera-dbgsym
```