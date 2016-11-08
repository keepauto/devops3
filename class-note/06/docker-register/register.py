
#!/usr/bin/python

import etcd
import sys
from urlparse import urlparse

etcd_host = "192.168.226.136:4001"
if not etcd_host:
    print "ETCD_HOST not set"
    sys.exit(1)

port = 4001
host = etcd_host

if ":" in etcd_host:
    host, port = etcd_host.split(":")

client = etcd.Client(host=host, port=int(port))

try:
    backends = client.read("/backends")
except (etcd.EtcdKeyNotFound, KeyError):
    client.write("/backends", None, dir=True)














# whoami-2

client.write("/backends/whoami/e9a5185ff67c", "192.168.226.136:32771", ttl=15)
client.write("/backends/whoami/port", "8000", ttl=15)










# whoami-1

client.write("/backends/whoami/13df60b3d5e9", "192.168.226.136:32770", ttl=15)
client.write("/backends/whoami/port", "8000", ttl=15)








