###
### Based on
### 

FROM opencv345

RUN uname -a

##
## Install build tools
##
RUN apt-get update
RUN apt-get install -y apt-utils
RUN apt-get install -y pkg-config
RUN apt-get install -y build-essential
RUN apt-get install -y cmake
RUN apt-get install -y git
RUN apt-get install -y unzip 
RUN apt-get install -y wget


##
## darknet installation
##
WORKDIR /
RUN git clone https://github.com/pjreddie/darknet.git
WORKDIR /darknet
# Set OpenCV makefile flag
RUN sed -i '/OPENCV=0/c\OPENCV=1' Makefile
RUN make
ENV DARKNET_HOME /darknet
ENV LD_LIBRARY_PATH /darknet

