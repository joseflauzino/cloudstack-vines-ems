#!/usr/bin/env python
import subprocess
import os
import time
import json
import logging
from util import *
from cloudstack_client_api import *

config = read_conf('auto_scaling','config.json')
cs = CloudstackWrapper()

def __main():
	module_name = 'auto_scaling'
	logging.warning("Scaling Agent is running now!")
	while True:
		to_scale = read_file(module_name,'to_scale')
		scaling = read_file(module_name,'scaling')
		i=0
		for vnf in to_scale['vnfs']:
			if is_vnf_in(vnf['vnf_id'],scaling['vnfs']):
				print "VNF com IP %s ja esta sendo escalada" % vnf['vnf_ip']
				job_status = get_job_status(vnf['job_id'])
				if job_status['status'] == 'done':
					print "Removendo vnf de scaling"
					index = 0
					for x in scaling['vnfs']:
						if x['vnf_id'] == vnf['vnf_id']:
							del scaling['vnfs'][index]
						index += 1
					if job_status['success'] == False: # VNF scale fail
						# TODO: add limit to try to scale a VNF
						continue # Keeps VNF in the to_scale list to try scale again
					print "Removendo vnf de to_scale"
					del to_scale['vnfs'][i]
					print "Zerando timeouts da vnf"
					vnf['policy']['scaleup']['timeouts'] = 0
					vnf['policy']['scaledown']['timeouts'] = 0
					print "Adicionando vnf em monitor"
					monitor = read_file(module_name,'monitor')
					monitor['vnfs'].append(vnf)
					save_file(module_name,'monitor',monitor)
					print "VNF escalada com sucesso!"
			else:
				logging.warning("New VNF to be escalated detected")
				logging.debug("Scaling VNF %s",vnf['vnf_id'])
				newserviceofferingid = vnf['policy'][vnf['action']]['newserviceofferingid']
				success,data = __scale_vnf(vnf['vnf_id'],newserviceofferingid)
				if success:
					vnf['job_id'] = data['recoveryvnfresponse']['jobid']
					print "Adicionando VNF em scaling"
					scaling['vnfs'].append(vnf)
			i+=1
		save_file(module_name,'to_scale',to_scale)
		save_file(module_name,'scaling',scaling)
		logging.debug("Waiting %s seconds",config['monitoringInterval'])
		time.sleep(config['monitoringInterval'])

def __scale_vnf(vnf_id,service_offering_id):
	return cs.scale_vnf(vnf_id,service_offering_id)

def run_scaling_agent():
    __main()