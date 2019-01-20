## deploy
```
fn --verbose deploy --app Darknet --local
```

## Run by invoke
To test if darknet is available execute:

```
fn invoke Darknet darknet_test
```

If al is ok, you should see answer similar to:

```
"<pydarknet.Detector object at 0x7fce33a25eb8>"
```

## Look into /functions directory
```
latestImage=$(docker images | grep darknet_test | head -1 | tr -s ' '| cut  -d ' ' -f3)
docker run --entrypoint "/bin/bash" -ti  $latestImage
```

