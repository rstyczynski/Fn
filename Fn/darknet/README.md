## deploy
```
fn --verbose deploy --app Darknet --local
```

## Run by invoke
```
time cat dog.jpg | fn invoke Darknet darknet
```

## Run by curl
```
time curl --data-binary "@dog.jpg" -X POST  http://localhost:8080/t/Darknet/darknet-trigger >out.jpg
```

## Look into /functions directory
```
latestImage=$(docker images | grep darknet | head -1 | tr -s ' '| cut  -d ' ' -f3)
docker run --entrypoint "/bin/bash" -ti  $latestImage
```

