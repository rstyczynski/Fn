# Fn
FnProject workbench

## set home
```
set fnw_home=/Users/rstyczynski/Developer/Fn/
```

## prepare docker images
```
cd $fnw_home/docker/opencv345  
docker build -t opencv345 .  
cd $fnw_home/docker/darknet  
docker build -t darknet .  
cd $fnw_home/docker/yolo3-4-py  
docker build -t yolo3-4-py .  
```

## start Fn server
Start fn server in a terminal.

```
fn start
```

## deploy function
Deploy function in another terminal.

```
cd $fnw_home/Fn/OpenCV
fn --verbose deploy --app OpenCV --local
```

## execute
Execute functions.


```
cd $fnw_home/Fn/OpenCV

time cat in.jpg | fn invoke OpenCV canny > out.jpg
## old: time cat in.jpg | base64 | fn invoke OpenCV canny | tr -d '"' | base64 -D >out1.jpg

time curl -d "$(cat in.jpg )" -X POST  http://localhost:8080/t/OpenCV/canny-trigger >out2.jpg
## old: time curl -d "$(cat in.jpg | base64)" -X POST  http://localhost:8080/t/OpenCV/canny-trigger | tr -d '"' | base64 -D >out2.jpg

##old: time cat hubert.jpg | base64 | fn invoke helloDN hellodn | tr -d '"' | base64 -D >hubert1.jpg
##old: time cat hubert.jpg | base64 > hubert.b64
##old: time curl --data-binary "@hubert.b64" -X POST  http://localhost:8080/t/helloDN/hellodn-trigger | tr -d '"' | base64 -D >hubert2.jpg

curl ---data-binary "@in.jpg" -X POST http://localhost:8080/t/OpenCV/canny-trigger>out2.jpg

```
## DEBUG
### get last call
fn list calls OpenCV canny | head -n 1
### get logs from last call
fn get logs OpenCV canny 01D16J3VY3NG8G00GZJ000004


