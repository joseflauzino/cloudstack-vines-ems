#!/usr/bin/env python

import os
import shlex, subprocess
import requests

#==================================================================
#                 Vines-Leaf Driver Implementation                 
#                                                by Jose Flauzino 
#==================================================================

def find_by_key(array, key):
	for d in array:
		for current_key, current_value in d.items():
			if current_key == key:
				return current_value
	return None

#------------------------------------------------------------------
# General methods
#------------------------------------------------------------------
def vnf_status(args):
	try:
		response = sendRequest("GET", _create_url(find_by_key(args,"vnf_ip"), "emsstatus"))
		return {'status':'success','data':response.text}
	except:
		return {'status':'success','data':'could not get vnf status'}

def status(args):
	try:
		response = sendRequest("GET", _create_url(find_by_key(args,"vnf_ip"), "running"))
		return {'status':'success','data':response.text}
	except:
		return {'status':'success','data':'could not get network function status'}

def push_vnfp(args):
	vnfp_path = find_by_key(args,"vnfp_path")
	url = _create_url(find_by_key(args,"vnf_ip"), "push_vnfp")
	function = open(vnfp_path, 'rb').read()
	try:
		response = requests.post(url, data=function, headers={'Content-Type': 'application/octet-stream'})
		print(response.text)
		return {'status':'success','data':response.text}
	except:
		return {'status':'success','data':'could not push vnfp (POST error)'}

	# Push the VNFP file to VNF
	#http_header = "--header \"Content-Type: application/zip\""
	#scp_cmd = "curl -i -X POST %s --data-binary @%s %s" % (http_header, vnfp_path, url)
	#response = run_shell_cmd(scp_cmd)
	#if response["status"] == "ERROR":
	#	return {'status':'error','data':"could not push vnfp (scp error)"}
	#return {'status':'success','data':response["data"]}

def install(args):
	try:
		response = sendRequest("POST", _create_url(find_by_key(args,"vnf_ip"), "install"))
		return {'status':'success','data':response.text}
	except:
		return {'status':'success','data':'could not install function'}

def start(args):
	try:
		response = sendRequest("POST", _create_url(find_by_key(args,"vnf_ip"), "start"))
		return {'status':'success','data':response.text}
	except:
		return {'status':'success','data':'could not start function'}

def stop(args):
	try:
		response = sendRequest("POST", _create_url(find_by_key(args,"vnf_ip"), "stop"))
		return {'status':'success','data':response.text}
	except:
		return {'status':'success','data':'could not stop function'}

def get_log(args):
	try:
		response = sendRequest("GET", _create_url(find_by_key(args,"vnf_ip"), "log"))
		return {'status':'success','data':response.text}
	except:
		return {'status':'success','data':'could not get function log'}


#------------------------------------------------------------------
# Vines-Leaf specific methods
#------------------------------------------------------------------
def _create_url(vnf_ip, task):
	return ''.join(['http://', vnf_ip, ':8000/api/', task])

def sendRequest(method, url)
	if method=="GET":
		response = requests.get(url)
	if method=="POST":
		response = requests.post(url)
	print(response)
	print(response.text)
	return response