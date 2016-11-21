#!/bin/sh

HOST_IP=192.168.226.134
ETCD_HOST=${HOST_IP}:4001
docker rm -f etcd-discovery
#docker run --name etcd-discovery -itd -p 4001:4001 -p 7001:7001 -v /var/etcd/:/data microbox/etcd:latest  /bin/etcd -addr ${ETCD_HOST}:4001 -peer-addr ${ETCD_HOST}:7001
#docker run --name etcd-discovery -itd -p 4001:4001 -p 7001:7001 -v /var/etcd/:/data microbox/etcd:latest -addr=${HOST_IP}:4001 -peer-addr=${HOST_IP}:7001


docker rm -f whoami-1
docker rm -f whoami-2
docker run -d -p :8000 --name whoami-1 -t jwilder/whoami
docker run -d -p :8000 --name whoami-2 -t jwilder/whoami

docker rm -f docker-register
docker run --name docker-register -d -e HOST_IP=$HOST_IP -e ETCD_HOST=$ETCD_HOST -v /var/run/docker.sock:/var/run/docker.sock -t jwilder/docker-register

docker rm -f docker-discover
docker run -d --net host --name docker-discover -e ETCD_HOST=$ETCD_HOST -p 1936:1936 -t jwilder/docker-discover python ./main.py
