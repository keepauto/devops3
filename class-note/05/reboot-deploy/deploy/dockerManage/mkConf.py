#!/usr/bin/env python
#coding:utf-8

from jinja2 import Template
import os

apps = [
{
   "name": "vote",
    "upstream": [
        {
           "host":"127.0.0.1",
           "port":1122
        },
        {
           "host":"127.0.0.1",
           "port":1133
        },
    ]
},
{
   "name": "check",
    "upstream": [
        {
           "host":"127.0.0.1",
           "port":1122
        },
        {
           "host":"127.0.0.1",
           "port":1133
        },
    ]
},
]

with open("nginx_conf/conf.d/default.conf.tpl") as f:
    with open("nginx_conf/conf.d/default.conf","w"):
        temp = Template(f.read())
        fw.write(temp.render(apps=apps))

print os.popen("docker exec nginx /usr/sbin/nginx -s reload").read()
