#!/usr/bin/env python

import os
import socket
from util import *

#==================================================================
#                  COVEN Driver Implementation 
#                
# Sep 2020              by Vinicius Fulber-Garcia and Jose Flauzino 
#==================================================================

def vnf_status(args):
	response = run_vnf_request_cmd(args, _build_cmd("status", args))
	if response["status"] == "ERROR":
		return {'status':'error','data':"could not get the VNF status"}
	return {'status':'success','data':response["data"]}


def status(args):
	return {'status':'error','data':'method unavailable'}


def push_vnfp(args):
	router_ip = find_by_key(args,"router_ip")
	vnfp_path = find_by_key(args,"vnfp_path")
	vnfp_filename = find_by_key(args,"vnfp_filename")
	# Push the VNFP zip file to router via SCP
	scp_cmd = "scp -i /root/.ssh/id_rsa.cloud -P 3922 %s root@%s:/root/" % (vnfp_path,router_ip)
	response = run_shell_cmd(scp_cmd)
	if response["status"] == "ERROR":
		return {'status':'error','data':"could not push the VNFP (scp error)"}
	# Push the socket_curl.py file to the router via SCP
	scp_cmd = "scp -i /root/.ssh/id_rsa.cloud -P 3922 %s root@%s:/root/" % ("socket_curl.py",router_ip)
	response = run_shell_cmd(scp_cmd)
	if response["status"] == "ERROR":
		return {'status':'error','data':"could not push the socket_curl.py file (scp error)"}
	# Push the VNFP zip file from the router to the VNF using the socket_curl.py file
	response = run_vnf_request_cmd(args, _build_cmd("install", args))
	if response["status"] == "ERROR":
		return {'status':'error','data':"could not push the VNFP"}
	return {'status':'success','data':response["data"]}


def install(args):
	return {'status':'success','data':"the network function was installed on the push_vnfp step"}


def start(args):
	response = run_vnf_request_cmd(args, _build_cmd("start", args))
	if response["status"] == "ERROR":
		return {'status':'error','data':"could not start the network function"}
	return {'status':'success','data':response["data"]}


def stop(args):
	response = run_vnf_request_cmd(args, _build_cmd("stop", args))
	if response["status"] == "ERROR":
		return {'status':'error','data':"could not stop the network function"}
	return {'status':'success','data':response["data"]}


#------------------------------------------------------------------
# COVEN specific methods
#------------------------------------------------------------------
origin_port = 1024
destination_port = 12345 # port where the COVEN is listen 

def _build_cmd(operation, args):
	# "python socket_curl.py <origin_ip> <origin_port> <destination_ip> <destination_port> \"<method_name>\" \"zip_file_path\""
	zip_file_path = ""
	if operation == "install":
		zip_file_path = "\"zip_file_path\""
	cmd = "python socket_curl.py %s %s %s %s \"%s\" %s" % (
		find_by_key(args,"router_ip"), origin_port, find_by_key(args,"vnf_ip"), destination_port, operation, zip_file_path)
	return cmd
