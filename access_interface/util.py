#!/usr/bin/env python

import os
import shlex, subprocess

ssh_key = "-i /root/.ssh/id_rsa.cloud"
#ssh_key = "-i /root/.ssh/teste"
ssh_port = "3922"
#ssh_port = "22"

def run_shell_cmd(cmd):
	process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
	output, error = process.communicate()
	if process.returncode != 0:
		print "Error on command"
		return {"status":"ERROR","data":output}
	output = output.rstrip("\n")
	if output == "":
		output = "None"
	return {"status":"SUCCESS","data":output}

def build_ssh_cmd(router_ip, cmd):
	ssh_cmd = "ssh %s %s -p %s %s" % (ssh_key, router_ip, ssh_port, cmd)
	return ssh_cmd

def run_vnf_request_cmd(args, cmd):
	router_ip = find_by_key(args,"router_ip")
	ssh_cmd = build_ssh_cmd(router_ip, cmd)
	return run_shell_cmd(ssh_cmd)

# For local test
def run_local_vnf_request_cmd(args, cmd):
	print cmd.strip("'")
	return run_shell_cmd(cmd.strip("'"))

def find_by_key(array, key):
	for d in array:
		for current_key, current_value in d.items():
			if current_key == key:
				return current_value
	return None