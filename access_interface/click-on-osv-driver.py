#!/usr/bin/env python

from util import *

#==================================================================
#                 Click-on-OSv Driver Implementation                 
#                                                by Jose Flauzino 
#==================================================================

#------------------------------------------------------------------
# General methods
#------------------------------------------------------------------

def vnf_status(args):
	cmd = _build_cmd("GET", _create_url(find_by_key(args,"vnf_ip"), "version"))
	response = run_vnf_request_cmd(args, cmd)
	#response = run_local_vnf_request_cmd(args, cmd)
	if response["status"] == "ERROR":
		return {'status':'error','data':"could not get vnf status"}
	return {'status':'success','data':'Running'}

def status(args):
	cmd = _build_cmd("GET", _create_url(find_by_key(args,"vnf_ip"), "running"))
	response = run_vnf_request_cmd(args, cmd)
	#response = run_local_vnf_request_cmd(args, cmd)
	if response["status"] == "ERROR":
		return {'status':'error','data':"could not get network function status"}
	return {'status':'success','data':response["data"]}

def push_vnfp(args):
	# TODO:
	#     - Save and unzip the VNFP
	#     - Read click function file
	#     - Write the Click Function on VNF
	#     - cmd example: curl -X POST 'http://192.168.122.127:8000/click_plugin/write_file?path=func.click&content=FromDPDKDevice(0)%20-%3E%20Print(%22Configured-By-Vines%22)%20-%3E%20Discard%3B'
	return {'status':'success','data':"OK"}

def install(args):
	return {'status':'success','data':'Function is installed on push_vnfp step'}

def start(args):
	cmd = _build_cmd("POST", _create_url(find_by_key(args,"vnf_ip"), "start"))
	response = run_vnf_request_cmd(args, cmd)
	#response = run_local_vnf_request_cmd(args, cmd)
	if response["status"] == "ERROR":
		return {'status':'error','data':"could not start function"}
	return {'status':'success','data':response["data"]}

def stop(args):
	cmd = _build_cmd("POST", _create_url(find_by_key(args,"vnf_ip"), "stop"))
	response = run_vnf_request_cmd(args, cmd)
	#response = run_local_vnf_request_cmd(args, cmd)
	if response["status"] == "ERROR":
		return {'status':'error','data':"could not stop function"}
	return {'status':'success','data':response["data"]}

def get_log(args):
	cmd = _build_cmd("GET", _create_url(find_by_key(args,"vnf_ip"), "log"))
	response = run_vnf_request_cmd(args, cmd)
	#response = run_local_vnf_request_cmd(args, cmd)
	if response["status"] == "ERROR":
		return {'status':'error','data':"could not get function log"}
	return {'status':'success','data':response["data"]}


#------------------------------------------------------------------
# Click-on-OSv specific methods
#------------------------------------------------------------------
def _create_url(vnf_ip, task):
	return ''.join(['http://', vnf_ip, ':8000/click_plugin/', task])

def _build_cmd(http_method, url):
	http_header = "--header \"Content-Type: application/json\""
	curl_cmd = "'curl -X %s %s %s'" % (http_method, http_header, url)
	return curl_cmd