#! /usr/bin/python3
# description       : Vines-Leaf Driver
# author            : Jose Flauzino
# email             : jwvflauzino@inf.ufpr.br
# date              : 20210127
# license           : Apache 2.0
# py version        : 3.6.9
#==============================================================================

import os
import shlex, subprocess
import requests

#------------------------------------------------------------------
# General methods
#------------------------------------------------------------------
def vnf_status(args):
	try:
		response = _sendRequest("GET", _create_url(_find_by_key(args,"vnf_ip"), "emsstatus"))
		return {'status':'success','data':response.text}
	except:
		return {'status':'success','data':'could not get vnf status'}

def status(args):
	try:
		response = _sendRequest("GET", _create_url(_find_by_key(args,"vnf_ip"), "running"))
		return {'status':'success','data':response.text}
	except:
		return {'status':'success','data':'could not get network function status'}

def push_vnfp(args):
	vnfp_path = _find_by_key(args,"vnfp_path")
	url = _create_url(_find_by_key(args,"vnf_ip"), "push_vnfp")
	function = open(vnfp_path, 'rb').read()
	try:
		response = requests.post(url, data=function, headers={'Content-Type': 'application/octet-stream'})
		print(response.text)
		return {'status':'success','data':response.text}
	except:
		return {'status':'success','data':'could not push vnfp (POST error)'}

def install(args):
	try:
		response = _sendRequest("POST", _create_url(_find_by_key(args,"vnf_ip"), "install"))
		return {'status':'success','data':response.text}
	except:
		return {'status':'success','data':'could not install function'}

def start(args):
	try:
		response = _sendRequest("POST", _create_url(_find_by_key(args,"vnf_ip"), "start"))
		return {'status':'success','data':response.text}
	except:
		return {'status':'success','data':'could not start function'}

def stop(args):
	try:
		response = _sendRequest("POST", _create_url(_find_by_key(args,"vnf_ip"), "stop"))
		return {'status':'success','data':response.text}
	except:
		return {'status':'success','data':'could not stop function'}

def get_log(args):
	try:
		response = _sendRequest("GET", _create_url(_find_by_key(args,"vnf_ip"), "log"))
		return {'status':'success','data':response.text}
	except:
		return {'status':'success','data':'could not get function log'}

#------------------------------------------------------------------
# Util
#------------------------------------------------------------------
def _create_url(vnf_ip, task):
	return ''.join(['http://', vnf_ip, ':8000/api/', task])

def _sendRequest(method, url):
	if method=="GET":
		response = requests.get(url)
	if method=="POST":
		response = requests.post(url)
	return response

def _find_by_key(array, key):
	for d in array:
		for current_key, current_value in d.items():
			if current_key == key:
				return current_value
	return None