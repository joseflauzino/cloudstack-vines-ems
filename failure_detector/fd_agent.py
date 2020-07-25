#!/usr/bin/env python
import time
import logging
from util import *

config = read_conf('failure_detector','config.json')

def __main():
    module_name = 'failure_detector'
    logging.warning("Failure Detector Agent is running now!")
    while True:
        logging.debug("Monitoring...")
        alive = read_file(module_name,'alive')
        i = 0
        for vnf in alive['vnfs']:
            detected = read_file(module_name,'detected')
            if not is_vnf_up(vnf['vnf_ip']):
                vnf['timeouts'] += 1
                logging.warning("[VNF_INACTIVE] VNF %s is inactive. Timeouts: %s",vnf['vnf_ip'],vnf['timeouts'])
                if vnf['timeouts'] >= 3:
                    logging.warning("[VNF_FAILURE] VNF "+vnf['vnf_ip']+" is down.")
                    detected['vnfs'].append(vnf)
                    del alive['vnfs'][i]
            else:
                if vnf['timeouts'] > 0:
                    vnf['timeouts'] = 0
                logging.info("[VNF_ACTIVE] VNF %s is active. Timeouts: %s",vnf['vnf_ip'],vnf['timeouts'])
            save_file(module_name,'alive',alive)
            save_file(module_name,'detected',detected)
            i+=1
        time.sleep(config['monitoringInterval'])

def run_fd_agent():
    __main()