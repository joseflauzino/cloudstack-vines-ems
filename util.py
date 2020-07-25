#!/usr/bin/env python
from datetime import datetime
import os
import subprocess
import json

def read_file(module_name, file_name):
    return json.loads(open(module_name+'/base/'+file_name, 'r').read())

def read_conf(module_name, file_name):
    return json.loads(open(module_name+'/'+file_name, 'r').read())

def read_global_conf(file_name):
    return json.loads(open(file_name, 'r').read())

def save_file(module_name, file_name,data):
    open(module_name+'/base/'+file_name, 'w+').write(json.dumps(data))

def is_vnf_up(ip):
    with open(os.devnull, "wb") as limbo:
        result=subprocess.Popen(["ping", "-c", "1", "-n", "-W", "2", ip],
                stdout=limbo, stderr=limbo).wait()
        if result:
            return False # VNF is crash
        else:
            return True # VNF is up

def is_vnf_in(vnf_id,data):
    result = False
    for vnf in data:
        if vnf['vnf_id'] == vnf_id:
            result = True
            break
    return result

def get_job_status(cloudstack_client, job_id):
    response = cloudstack_client.get_job_status(job_id)
    response = response['queryasyncjobresultresponse']
    if response['jobstatus'] != 0:
        if response['jobresultcode'] != 0:
            return {'status':'done','success':False} # the Job ended in error
        return {'status':'done','success':True} # the Job ended succefully
    return {'status':'loading','success':True} # Loading