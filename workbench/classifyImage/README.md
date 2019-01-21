Authentication
==============

Access control checks client name, by comparing privided client name (AUTH) with names registered in configuration. Access control requires to provide invoke token (TOKEN), which has to be taken from GET call to /status. Token guarantees that single client will not consume all resources. 

Get image classification
========================
Darknet example.



Terminal #1:

```
python3 classifyImage.py 
```

Terminal #2:

```
CLIENT=client1
time TOKEN=$(curl "http://localhost:5002/status?AUTH=$CLIENT" | grep TOKEN | cut -d'"' -f4)
time curl -X POST -F name=Test -F filedata=@banker.jpeg "http://localhost:5002/classify?AUTH=$CLIENT&TOKEN=$TOKEN" 
```


Get image dimensions
====================
OpenCV example.



Terminal #1:

```
python3 measureImage.py 
```


Terminal #2:

```
CLIENT=client1
time TOKEN=$(curl "http://localhost:5002/status?AUTH=$CLIENT" | grep TOKEN | cut -d'"' -f4)
time curl -X POST -F name=Test -F filedata=@banker.jpeg "http://localhost:5002/dimensions?AUTH=$CLIENT&TOKEN=$TOKEN" 
```

Get image convrted by canny filter
==================================
OpenCV example.



Terminal #1:

```
python3 convertImage.py 
```


Terminal #2:

```
CLIENT=client1
time TOKEN=$(curl "http://localhost:5002/status?AUTH=$CLIENT" | grep TOKEN | cut -d'"' -f4)
time curl -X POST -F name=Test -F filedata=@banker.jpeg "http://localhost:5002/canny?AUTH=$CLIENT&TOKEN=$TOKEN"  --output out.jpg
```
