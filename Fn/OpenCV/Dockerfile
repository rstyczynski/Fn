FROM yolo3-4-py
WORKDIR /function
ADD . /function/

RUN pip3 install --target /python/  --no-cache --no-cache-dir -r requirements.txt 

RUN rm -fr ~/.cache/pip /tmp* requirements.txt func.yaml Dockerfile .venv

ENV PYTHONPATH=/python
ENTRYPOINT ["python3", "canny.py"]
