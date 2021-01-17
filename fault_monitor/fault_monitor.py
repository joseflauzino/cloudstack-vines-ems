#! /usr/bin/python3
# description       : CloudStack Vines EMS - Fault Monitor Module
# author            : Jose Flauzino
# email             : jwvflauzino@inf.ufpr.br
# date              : 20210113
# license           : Apache 2.0
# py version        : 3.6.9
#==============================================================================

import threading
import signal
import os
import sys
import requests
from pathlib import Path
from time import sleep
import logging
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
#print(parentdir)
sys.path.insert(0,parentdir)
from vib.vib_client import *

logging.basicConfig(filename='fault_monitor.log', level=logging.DEBUG)

##################################################################
######################## Fault Monitor ###########################
##################################################################

threads = []

def _notifyVnfm(vnf_id):
	logging.info("Notifying VNFM about VNF "+vnf_id)

def _reload_active_policies(interval=None):
	result = find_policy()
	if result["success"] == False:
		raise
	active_policies = []
	if interval != None: # select by monitoring interval
		for policy in result["data"]:
			if policy["state"] == "active" and policy["monitoring_interval"] == interval:
				logging.info("Adding policy "+str(policy["monitoring_interval"])+" in thread "+str(interval))
				active_policies.append(policy)
	else: # select all active policies
		for policy in result["data"]:
			if policy["state"] == "active":
				active_policies.append(policy)
	return active_policies

def get_modfication_date():
	last_modification = Path(parentdir)/'vib/policy_base.json'
	return last_modification.stat().st_mtime

def _test_vnf(vnf_ip):
	try:
		response = requests.get("http://"+vnf_ip+":8000/api/emsstatus", timeout=0.01)
		return True
	except:
		return False

def monitoring(interval):
	initial_modification = get_modfication_date()
	active_policies = _reload_active_policies(interval)
	number_of_active_policies = len(active_policies)
	while number_of_active_policies > 0:
		for policy in active_policies:
			result = find_vnf(policy["vnf_id"])
			if result["success"] == False:
				raise
			if _test_vnf(result["data"][0]["ip"]) == False:
				logging.info("[thread "+str(interval)+"] VNF "+result["data"][0]["ip"]+" is inactive")
				_notifyVnfm(result["data"][0]["id"])
			else:
				logging.info("[thread "+str(interval)+"] VNF "+result["data"][0]["ip"]+" is active")
		sleep(interval)
		new_modfication_date = get_modfication_date()
		if initial_modification < new_modfication_date:
			initial_modification = new_modfication_date
			active_policies = _reload_active_policies(interval)
			number_of_active_policies = len(active_policies)
	logging.info("Thread "+str(interval)+" ended")


def _create_monitoring_groups(active_policies):
	monitoring_groups = []
	for policy in active_policies:
		if policy["monitoring_interval"] not in monitoring_groups:
			monitoring_groups.append(policy["monitoring_interval"])
	return monitoring_groups

def get_thread_names():
	names = []
	for t in threads:
		names.append(t.name)
	return names

def create_threads(active_policies):
	monitoring_groups = _create_monitoring_groups(active_policies)
	for group in monitoring_groups:
		if len(threads) > 0: # there are created threads
			if str(group) not in get_thread_names():
				threads.append(threading.Thread(target=monitoring, name=str(group), args=(group,)))
		else: # thread list is empty
			threads.append(threading.Thread(target=monitoring, name=str(group), args=(group,)))

def start_threads():
	for t in threads:
		try:
			t.start()
		except Exception as e:
			pass

def _stop_threads():
	logging.debug("Stopping Fault Monitor")
	os.kill(os.getpid(), signal.SIGTERM)

def check_for_changing(started_point):
	new_modfication_date = get_modfication_date()
	if started_point < new_modfication_date:
		started_point = new_modfication_date
		active_policies = _reload_active_policies()
		number_of_vnfs = len(active_policies)
		create_threads(active_policies)
		start_threads()
		return new_modfication_date
	return started_point

def garbage_collector():
	for t in threads:
		if t.is_alive() == False:
			del threads[threads.index(t)]

def main():
	started_point = get_modfication_date()
	active_policies = _reload_active_policies()
	create_threads(active_policies)
	start_threads()

	while True:
		started_point = check_for_changing(started_point)
		garbage_collector()
		sleep(2)


if __name__ == '__main__':
	try:
		logging.debug("Fault Monitor is running now!")
		main()
	except (KeyboardInterrupt):
		_stop_threads()