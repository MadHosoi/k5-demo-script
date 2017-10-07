# Local

docker build -t madhosoi/k5websample:v.1.0 .
docker push madhosoi/k5websample:v.1.0

cf login
cf apps
cf push
