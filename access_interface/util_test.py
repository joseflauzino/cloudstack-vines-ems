#!/usr/bin/env python

from util import *

cmd = "ssh -i /root/.ssh/id_rsa.cloud 169.254.0.129 -p 3922 'curl -X GET --header \"Content-Type: application/json\" http://10.1.1.156:8000/api/emsstatus'"
print run_shell_cmd(cmd)