#!/usr/bin/env python
import json
import os
import requests

url = 'http://localhost:9000/v1.0/vnf/pushvnfp/b4abb154-9be4-4afe-a84a-c19b3747b9ca'
files = {
    'file': (os.path.basename("/var/www/html/vnfp/apache2-vines-leaf.zip"), open("/var/www/html/vnfp/apache2-vines-leaf.zip", 'rb'), 'application/octet-stream')
}
response = requests.post(url, files=files)
print response
