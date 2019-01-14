##
## Image size
##
# 789MB
#

###
### Based on
### 
# https://github.com/docker-library/python/blob/721671c28aad96ad2c1970e83c2af71ceff15f1b/3.6/stretch/slim/Dockerfile
# 1. python:3.6-slim-stretch
#    >> https://github.com/docker-library/python/blob/721671c28aad96ad2c1970e83c2af71ceff15f1b/3.6/stretch/slim/Dockerfile
# 2. debian:stretch-slim
#    >> https://github.com/debuerreotype/docker-debian-artifacts/blob/223b1234e2bcd3248b7e8feb86b8aedd00e5487f/stretch/slim/Dockerfile

##
## OpenCV 3.4 installation
##
# 1. https://docs.opencv.org/3.4.5/d7/d9f/tutorial_linux_install.html

##
## OpenCV 3.4 docker installation
##
# 1. https://hub.docker.com/r/jjanzic/docker-python3-opencv/dockerfile

##
## Rules
##
#  1. Avoid mutiple RUN to keep image small 

##
## Docker directives
##
FROM python:3.6-slim-stretch

RUN uname -a

##
## Install 
##
RUN apt-get update && \
        apt-get install -y \
        build-essential \
        cmake \
        git \
        wget \
        unzip \
        yasm \
        pkg-config \
        libswscale-dev \
        libtbb2 \
        libtbb-dev \
        libjpeg-dev \
        libpng-dev \
        libtiff-dev \
        libavformat-dev \
        libpq-dev && \
    echo && \ 
    echo Python libs && \
    echo && \ 
    pip3 install pkgconfig cython numpy && \
    echo && \ 
    echo OpenCV install && \
    echo && \ 
    wget https://github.com/opencv/opencv/archive/3.4.5.zip && \
    unzip 3.4.5.zip && \
    rm 3.4.5.zip && \
    mkdir /build && \
    cd /build && \
    cmake \
      -D BUILD_EXAMPLES=OFF \
      -D BUILD_opencv_python3=ON \
      /opencv-3.4.5 && \
    make -j4 && \
    make install && \
    ldconfig &&\
    echo && \ 
    echo Cleanup && \
    echo && \ 
    rm -r /build && \
    rm -r /opencv-3.4.5 && \
    apt-get autoremove -y && \
    apt-get remove -y unzip wget git build-essential cmake pkg-config apt-utils

CMD python3 -c 'import cv2; print("OpenCV " + cv2.__version__ + " ready.")'

	