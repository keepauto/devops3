#!/bin/sh

HOST_DIR=~/open-falcon
DOCKER_DIR=/home/work/open-falcon

docker rm -f ${LOGNAME}-of
docker run -td --name ${LOGNAME}-of -v $HOST_DIR/conf:$DOCKER_DIR/conf -v $HOST_DIR/data:$DOCKER_DIR/data -v $HOST_DIR/logs:$DOCKER_DIR/logs -v $HOST_DIR/mysql:$DOCKER_DIR/mysql -p 8413:8433 -p 6013:6030 -p 5015:5050 -p 8018:8080 -p 8011:8081 -p 6010:6060 -p 5010:5090 registry.4paradigm.com/open-falcon:latest
