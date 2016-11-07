#!/bin/sh

HOST_IP=59.110.12.72
ETCD_HOST=${HOST_IP}:4001
docker rm -f docker-register
docker run --name docker-register -d -e HOST_IP=$HOST_IP -e ETCD_HOST=$ETCD_HOST -v /var/run/docker.sock:/var/run/docker.sock -t jwilder/docker-register


docker rm -f whoami-1
docker rm -f whoami-2
docker run -d -p :8000 --name whoami-1 -t jwilder/whoami
docker run -d -p :8000 --name whoami-2 -t jwilder/whoami

docker rm -f docker-register
docker run --name docker-register -d -e HOST_IP=$HOST_IP -e ETCD_HOST=$ETCD_HOST -v /var/run/docker.sock:/var/run/docker.sock -t jwilder/docker-register

docker rm -f docker-discover
docker run -d --net host --name docker-discover -e ETCD_HOST=$ETCD_HOST -p 1936:1936 -t jwilder/docker-discover
