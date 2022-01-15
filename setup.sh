#!/bin/sh
sudo apt update
sudo apt upgrade
sudo apt install build-essential cmake pkg-config
sudo apt install libjpeg-dev libtiff5-dev libjasper-dev libpng-dev
sudo apt install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
sudo apt install libxvidcore-dev libx264-dev
sudo apt install libatlas-base-dev gfortran
sudo apt install libhdf5-dev libhdf5-serial-dev libhdf5-103
sudo apt install libqt5gui5 libqt5webkit5 libqt5test5 python3-pyqt5
sudo apt install python3-dev
pip3 install opencv-python
pip3 install -r requirements.txt