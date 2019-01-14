###
### Based on
### 

FROM darknet

RUN uname -a

ENV DARKNET_HOME /darknet
ENV LD_LIBRARY_PATH /darknet

##
## YOLO3-4-Py installation
##
# https://github.com/madhawav/YOLO3-4-Py/blob/master/docker/Dockerfile

WORKDIR /
RUN git clone https://github.com/madhawav/YOLO3-4-Py.git
WORKDIR /YOLO3-4-Py
RUN python3 setup.py build_ext --inplace

##
## Run test ##
RUN sh download_models.sh
##

ADD ./docker_demo.py /YOLO3-4-Py/docker_demo.py
CMD ["python3", "docker_demo.py"]

