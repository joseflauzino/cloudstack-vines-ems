#!/usr/bin/env python

import urllib2
import urllib
import hashlib
import hmac
import base64
import time
import os
import uuid
import json
from datetime import datetime # logs

# Print formated logs
def print_log(msg_type, event, msg):
	print "[%s] [%s] [%s] %s" % (datetime.now(), msg_type, event, msg)

def read_file(file_name):
    return json.loads(open('base/'+file_name, 'r').read())

def save_file(file_name,data):
    open('base/'+file_name, 'w+').write(json.dumps(data))

def test(ip):
    with open(os.devnull, "wb") as limbo:
        result=subprocess.Popen(["ping", "-c", "1", "-n", "-W", "2", ip],
                stdout=limbo, stderr=limbo).wait()
        if result:
            # VNF is crash
            return False
        else:
            return True

class CloudstackWrapper():
	global request
	request = {}
	global management_server_ip
	management_server_ip = '192.168.122.94'

	# Return the apikey used to authenticate requests
	def get_apikey(self):
		return 'qEtYS7aPJ1iJXI1ULXgMJWFZe1Bky4MllXpevYecqL-xGzeZpFCvqsfXcG4tzp5zgvBVjKoiFFOYLpRZfae0KQ'


	# Return the secretkey used to authenticate requests
	def get_secretkey(self):
		return 'JNfk2kJxXaEyD_ZAQSu5b0NCtBj6LpkkgLcFfNdpNSDyc4DUqTVUKYOIRDcSSkCyWxDEEhtQIta7hXP2ZLPvWA'


	# Generate authenticates URLs
	def generate_url(self):
		baseurl='http://%s:8080/client/api?' % management_server_ip
		request_str='&'.join(['='.join([k,urllib.quote_plus(request[k])]) for k in request.keys()])
		sig_str='&'.join(['='.join([k.lower(),urllib.quote_plus(request[k].lower().replace('+','%20'))])for k in sorted(request.iterkeys())])
		sig=hmac.new(self.get_secretkey(),sig_str,hashlib.sha1)
		sig=hmac.new(self.get_secretkey(),sig_str,hashlib.sha1).digest()
		sig=base64.encodestring(hmac.new(self.get_secretkey(),sig_str,hashlib.sha1).digest())
		sig=base64.encodestring(hmac.new(self.get_secretkey(),sig_str,hashlib.sha1).digest()).strip()
		sig=urllib.quote_plus(base64.encodestring(hmac.new(self.get_secretkey(),sig_str,hashlib.sha1).digest()).strip())
		url=baseurl+request_str+'&signature='+sig
		return url


	# Get job status
	def get_job_status(self,job_id):
		command = 'queryAsyncJobResult'
		request.clear()
		request['command']=command
		request['jobid']=job_id
		request['response']='json'
		request['apikey']= self.get_apikey()	
		url = self.generate_url()
		try:
			response=urllib2.urlopen(url)
			response = response.read()
		except Exception as e:
			return (-1, "Could not get Job Status (URL error) - %s" % e)
		response = json.loads(response)
		return response


	# Get VM info
	def list_vm(self,vm_id):
		command = 'listVirtualMachines'
		request.clear()
		request['command']=command
		request['id']=vm_id
		request['response']='json'
		request['apikey']= self.get_apikey()	
		url = self.generate_url()
		try:
			response=urllib2.urlopen(url)
			response = response.read()
		except Exception as e:
			return (-1, "Could not list VMs (URL error) - %s" % e)
		response = json.loads(response)
		return response


	def stop_vm(self,vm_id):
		command = 'stopVirtualMachine'
		request.clear()
		request['command']=command
		request['id']=vm_id
		request['forced']='true'
		request['response']='json'
		request['apikey']= self.get_apikey()	
		url = self.generate_url()
		try:
			response=urllib2.urlopen(url)
			response = response.read()
		except Exception as e:
			return (-1, "Could not stop vm (URL error) - %s" % e)
		response = json.loads(response)
		return response

	def start_vm(self,vm_id):
		command = 'startVirtualMachine'
		request.clear()
		request['command']=command
		request['id']=vm_id
		request['response']='json'
		request['apikey']= self.get_apikey()	
		url = self.generate_url()
		try:
			response=urllib2.urlopen(url)
			response = response.read()
		except Exception as e:
			return (-1, "Could not start vm (URL error) - %s" % e)
		response = json.loads(response)
		return response

	def scale_vm(self,vm_id,service_offering_id):
		command = 'scaleVirtualMachine'
		request.clear()
		request['command']=command
		request['id']=vm_id
		request['serviceofferingid']=service_offering_id
		request['response']='json'
		request['apikey']= self.get_apikey()	
		url = self.generate_url()
		try:
			response=urllib2.urlopen(url)
			response = (True, response.read())
		except Exception as e:
			return (False, e)
		return response