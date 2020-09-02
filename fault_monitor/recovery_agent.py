#!/usr/bin/env python
import subprocess
import os
import time
import json
import logging
from util import *
from cloudstack_api_client import *

config = read_conf('failure_detector','config.json')
cs = CloudstackWrapper()

def __main():
	module_name = 'failure_detector'
	logging.warning("Recovery Agent is running now!")
	while True:
		detected = read_file(module_name,'detected')
		recovery = read_file(module_name,'recovery')
		i=0
		for vnf in detected['vnfs']:
			if is_vnf_in(vnf['vnf_id'],recovery['vnfs']):
				logging.info("VNF %s is being recovered", vnf['vnf_id'])
				job_status = get_job_status(cs, vnf['job_id'])
				if job_status['status'] == 'done':
					logging.debug("Removing VNF %s from the recovery list", vnf['vnf_id'])
					index = 0
					for x in recovery['vnfs']:
						if x['vnf_id'] == vnf['vnf_id']:
							del recovery['vnfs'][index]
						index += 1
					if job_status['success'] == False: # VNF recovery fail
						# TODO: add limit to try to recovery a VNF
						continue # Keeps VNF in the detected list to try recover again
					logging.debug("Removing VNF %s from the detected list", vnf['vnf_id'])
					del detected['vnfs'][i]
					logging.debug("Removing VNF %s from the detected list", vnf['vnf_id'])
					logging.debug("Resetting VNF %s timeouts",vnf['vnf_id'])
					vnf['timeouts'] = 0
					logging.debug("Adding VNF %s to the alive list", vnf['vnf_id'])
					alive = read_file(module_name,'alive')
					alive['vnfs'].append(vnf)
					save_file(module_name,'alive',alive)
					logging.info("VNF %s successfully recovered!",vnf['vnf_id'])
			else:
				logging.warning("New crashed VNF detected")
				logging.info("Asking to VNFM recover the VNF %s", vnf['vnf_id'])
				success,data = __recovery_vnf(vnf['vnf_id'])
				if success:
					vnf['job_id'] = data['recoveryvnfresponse']['jobid']
					logging.debug("Adding VNF %s to the recovery list", vnf['vnf_id'])
					recovery['vnfs'].append(vnf)
				else:
					print "Error: %s" % data
			i+=1
		save_file(module_name,'detected',detected)
		save_file(module_name,'recovery',recovery)
		logging.debug("Waiting %s seconds",config['monitoringInterval'])
		time.sleep(config['monitoringInterval'])

def __recovery_vnf(vnf_id):
	return cs.recovery_vnf(vnf_id)

def run_recovery_agent():
    __main()