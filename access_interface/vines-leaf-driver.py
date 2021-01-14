#!/usr/bin/env python

import os
import sys
currentdir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(currentdir)
from util import *

#==================================================================
#                 Vines-Leaf Driver Implementation                 
#                                                by Jose Flauzino 
#==================================================================

#------------------------------------------------------------------
# General methods
#------------------------------------------------------------------
def vnf_status(args):
	cmd = _build_cmd("GET", _create_url(find_by_key(args,"vnf_ip"), "emsstatus"))
	response = run_local_vnf_request_cmd(args, cmd)
	if response["status"] == "ERROR":
		return {'status':'error','data':"could not get vnf status"}
	return {'status':'success','data':response["data"]}

def status(args):
	cmd = _build_cmd("GET", _create_url(find_by_key(args,"vnf_ip"), "running"))
	response = run_local_vnf_request_cmd(args, cmd)
	if response["status"] == "ERROR":
		return {'status':'error','data':"could not get network function status"}
	return {'status':'success','data':response["data"]}

def push_vnfp(args):
	vnfp_path = find_by_key(args,"vnfp_path")
	url = _create_url(find_by_key(args,"vnf_ip"), "push_vnfp")
	# Push the VNFP file to VNF
	http_header = "--header \"Content-Type: application/zip\""
	scp_cmd = "curl -i -X POST %s --data-binary @%s %s" % (http_header, vnfp_path, url)
	response = run_shell_cmd(scp_cmd)
	if response["status"] == "ERROR":
		return {'status':'error','data':"could not push vnfp (scp error)"}
	return {'status':'success','data':response["data"]}

def install(args):
	cmd = _build_cmd("POST", _create_url(find_by_key(args,"vnf_ip"), "install"))
	response = run_local_vnf_request_cmd(args, cmd)
	if response["status"] == "ERROR":
		return {'status':'error','data':"could not install function"}
	return {'status':'success','data':response["data"]}

def start(args):
	cmd = _build_cmd("POST", _create_url(find_by_key(args,"vnf_ip"), "start"))
	response = run_local_vnf_request_cmd(args, cmd)
	if response["status"] == "ERROR":
		return {'status':'error','data':"could not start function"}
	return {'status':'success','data':response["data"]}

def stop(args):
	cmd = _build_cmd("POST", _create_url(find_by_key(args,"vnf_ip"), "stop"))
	response = run_local_vnf_request_cmd(args, cmd)
	if response["status"] == "ERROR":
		return {'status':'error','data':"could not stop function"}
	return {'status':'success','data':response["data"]}

def get_log(args):
	cmd = _build_cmd("GET", _create_url(find_by_key(args,"vnf_ip"), "log"))
	response = run_local_vnf_request_cmd(args, cmd)
	if response["status"] == "ERROR":
		return {'status':'error','data':"could not get function log"}
	return {'status':'success','data':response["data"]}


#------------------------------------------------------------------
# Vines-Leaf specific methods
#------------------------------------------------------------------
def _create_url(vnf_ip, task):
	return ''.join(['http://', vnf_ip, ':8000/api/', task])

def _build_cmd(http_method, url):
	http_header = "--header \"Content-Type: application/json\""
	curl_cmd = "'curl -X %s %s %s'" % (http_method, http_header, url)
	return curl_cmd