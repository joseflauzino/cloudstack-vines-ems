#!/usr/bin/env python

import subprocess
import logging
import os
import time
import json
from utils import *
from em_client import *

def __main():
    logging.warning("MCPA is running now!")
    while True:
        monitor = read_file(module_name,'monitor')
        i=0
        for vnf in monitor['vnfs']:
            logging.debug("Monitoring...")
            to_scale = read_file(module_name,'to_scale')
            metrics = __get_metrics(vnf['vnf_ip'])
            logging.debug("Checking metrics of VNF")
            response = check_metrics(vnf['vnf_id'],metrics)
            if response['check_metrics'] == False:
                vnf['policy'][response['action']]['timeouts'] += 1
                if vnf['policy'][response['action']]['timeouts'] > vnf['policy'][response['action']]['maxtimeouts']:
                    del monitor['vnfs'][i]
                    vnf['action'] = response['action']
                    logging.debug("Adding VNF to %s",vnf['action'])
                    to_scale['vnfs'].append(vnf)
            else:
                logging.debug("VNF metrics is ok")
                if vnf['policy']['scaleup']['timeouts'] > 0:
                    vnf['policy']['scaleup']['timeouts'] = 0
                if vnf['policy']['scaledown']['timeouts'] > 0:
                    vnf['policy']['scaledown']['timeouts'] = 0
            save_file(module_name,'monitor',monitor)
            save_file(module_name,'to_scale',to_scale)  
            i+=1
        time_delay = int(read_file(module_name,'config.json')['config']['timedelay'])
        time.sleep(time_delay)

def check_metrics(vnf_id,metrics):
    module_name = 'auto_scaling'
    monitor = read_file(module_name,'monitor')
    policy = ''
    for vnf in monitor['vnfs']:
        if vnf['vnf_id']==vnf_id:
            policy = vnf['policy']
    cpu = 0
    memory = 0
    disk = 0
    for x in metrics['list']:
        if x['type']=="cpu":
            cpu = "%.2f" % float(x['percent_usage'])
            cpu = float(cpu)
            continue
        elif x['type']=="memory":
            memory = "%.2f" % float(x['percent_usage'])
            memory = float(memory)
            continue
        elif x['type']=="disk":
            disk = "%.2f" % float(x['percent_usage'])
            disk = float(disk)
            continue
        else:
            pass
    policy_scaleup = policy['scaleup']
    if (cpu >= policy_scaleup['cpu']['maxusage']) or (memory >= policy_scaleup['memory']['maxusage']):
        logging.warning("Resource usage is very high: cpu=%s, mem=%s",cpu,memory)
        return {"check_metrics":False,"action":"scaleup"}
    policy_scaledown = policy['scaledown']
    if (cpu <= policy_scaledown['cpu']['minusage']) or (memory <= policy_scaledown['memory']['minusage']):
        logging.warning("Resource usage is very low: cpu=%s, mem=%s",cpu,memory)
        return {"check_metrics":False,"action":"scaledown"}
    logging.debug("Resource usage is ok: cpu=%s, mem=%s",cpu,memory)
    return {"check_metrics":True,"action":None}

def __get_metrics(vnf_ip):
    em_client = ElementManagementClient()
    return em_client.get_metrics(vnf_ip).json()

def run_mcpa():
    __main()