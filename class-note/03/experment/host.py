#!/usr/bin/env python

# http://docs.ansible.com/ansible/developing_inventory.html
host_map = {
    "docker": {
        "hosts": ["aliyun-prophet-docker1", "aliyun-prophet-test1"]
    },
    "luojilab": {
        "hosts": [
            "aliyun-luojilab-predict1",
            "aliyun-luojilab-prophet1",
            "aliyun-luojilab-hdp1",
        ]
    },
    "prophet_demo": {
        "hosts": [
            "aliyun-prophet-demo1",
            "aliyun-prophet-docker1",
            "aliyun-prophet-test2"
        ]
    },
    "rbt": {
        "hosts": ["teach"]
    },
    "aliyun": {
        "children": ["prophet_demo"]
    },
}

import json
print json.dumps(host_map, indent=1)
