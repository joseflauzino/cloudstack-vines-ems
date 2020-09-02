#!/usr/bin/env python

from util import *

#==================================================================
#                 Vines-Leaf Driver Implementation                 
#                                                by Jose Flauzino 
#==================================================================

#------------------------------------------------------------------
# General methods
#------------------------------------------------------------------
def vnf_status(args):
	cmd = _build_cmd(_create_url(find_by_key(args,"vnf_ip"), "emsstatus"))
	response = run_vnf_request_cmd(args, cmd)
	if response["status"] == "ERROR":
		return {'status':'error','data':"could not get vnf status"}
	return {'status':'success','data':response}

def nf_status(args):
	cmd = _build_cmd(_create_url(find_by_key(args,"vnf_ip"), "running"))
	response = run_vnf_request_cmd(args, cmd)
	if response["status"] == "ERROR":
		return {'status':'error','data':"could not get network function status"}
	return {'status':'success','data':response}

def push_vnfp(args):
	router_ip = find_by_key(args,"router_ip")
	vnfp_path = find_by_key(args,"vnfp_path")
	vnfp_filename = find_by_key(args,"vnfp_filename")
	url = _create_url(find_by_key(args,"vnf_ip"), "push_vnfp")
	# Push the VNFP file to router via SCP
	scp_cmd = "scp -i /root/.ssh/id_rsa.cloud -P 3922 %s root@%s:/root/" % (vnfp_path,router_ip)
	response = run_shell_cmd(scp_cmd)
	if response["status"] == "ERROR":
		return {'status':'error','data':"could not push vnfp (scp error)"}
	# Push the VNFP file from router to VNF via HTTP (curl command)
	curlCmd = "'curl -i -X POST %s --data-binary @/root/%s %s'" % (http_header, vnfp_filename, url)
	ssh_cmd = "ssh -i /root/.ssh/id_rsa.cloud %s -p 3922 %s" % (router_ip,curlCmd)
	response = run_shell_cmd(ssh_cmd)
	if response["status"] == "ERROR":
		return {'status':'error','data':"could not push vnfp (ssh error)"}
	return {'status':'success','data':response}

def install(args):
	cmd = _build_cmd(_create_url(find_by_key(args,"vnf_ip"), "install"))
	response = run_vnf_request_cmd(args, cmd)
	if response["status"] == "ERROR":
		return {'status':'error','data':"could not install function"}
	return {'status':'success','data':response}

def start(args):
	cmd = _build_cmd(_create_url(find_by_key(args,"vnf_ip"), "start"))
	response = run_vnf_request_cmd(args, cmd)
	if response["status"] == "ERROR":
		return {'status':'error','data':"could not start function"}
	return {'status':'success','data':response}

def stop(args):
	cmd = _build_cmd(_create_url(find_by_key(args,"vnf_ip"), "stop"))
	response = run_vnf_request_cmd(args, cmd)
	if response["status"] == "ERROR":
		return {'status':'error','data':"could not stop function"}
	return {'status':'success','data':response}

def get_log(args):
	cmd = _build_cmd(_create_url(find_by_key(args,"vnf_ip"), "log"))
	response = run_vnf_request_cmd(args, cmd)
	if response["status"] == "ERROR":
		return {'status':'error','data':"could not get function log"}
	return {'status':'success','data':response}


#------------------------------------------------------------------
# Vines-Leaf specific method
#------------------------------------------------------------------
def _create_url(vnf_ip, task):
	return ''.join(['http://', vnf_ip, ':8000/api/', task])

def _build_cmd(url):
	http_header = "--header \"Content-Type: application/json\""
	curl_cmd = "'curl -X POST %s %s'" % (http_header, url)
	return curl_cmd