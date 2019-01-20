FROM yolo3-4-py
WORKDIR /function
ADD . /function/

RUN pip3 install --target /python/  --no-cache --no-cache-dir -r requirements.txt 

RUN rm -fr ~/.cache/pip /tmp* requirements.txt func.yaml Dockerfile .venv
RUN cp /YOLO3-4-Py/pydarknet.cpython-36m-x86_64-linux-gnu.so /function && \
    cp -r /YOLO3-4-Py/cfg /function && \
    cp -r /YOLO3-4-Py/data /function && \
    cp -r /YOLO3-4-Py/weights /function

ENV PYTHONPATH=/python
ENTRYPOINT ["python3", "darknet_test.py"]
