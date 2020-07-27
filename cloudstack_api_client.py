#!/usr/bin/env python

import urllib2
import urllib
import hashlib
import hmac
import base64
import json
from util import read_global_conf

class CloudstackWrapper():
	"""Implementation of CloudStack's REST API Client."""

	def __init__(self):
		self.global_conf = read_global_conf('em_conf.json')

	def __get_apikey(self):
		return self.global_conf['apiKey']

	def __get_secretkey(self):
		return self.global_conf['secretKey']

	def __request_factory(self, cmd):
		request = {}
		request['command']=cmd
		request['response']='json'
		request['apikey']= self.__get_apikey()
		return request

	def __generate_url(self, request):
		baseurl='http://%s:8080/client/api?' % self.global_conf['managementServerIp']
		request_str='&'.join(['='.join([k,urllib.quote_plus(request[k])]) for k in request.keys()])
		sig_str='&'.join(['='.join([k.lower(),urllib.quote_plus(request[k].lower().replace('+','%20'))])for k in sorted(request.iterkeys())])
		sig=hmac.new(self.__get_secretkey(),sig_str,hashlib.sha1)
		sig=hmac.new(self.__get_secretkey(),sig_str,hashlib.sha1).digest()
		sig=base64.encodestring(hmac.new(self.__get_secretkey(),sig_str,hashlib.sha1).digest())
		sig=base64.encodestring(hmac.new(self.__get_secretkey(),sig_str,hashlib.sha1).digest()).strip()
		sig=urllib.quote_plus(base64.encodestring(hmac.new(self.__get_secretkey(),sig_str,hashlib.sha1).digest()).strip())
		return baseurl+request_str+'&signature='+sig

	def get_job_status(self,job_id):
		request = self.__request_factory('queryAsyncJobResult')
		request['jobid']=job_id
		url = self.__generate_url(request)
		try:
			response = urllib2.urlopen(url).read()
		except:
			return (-1, "CLOUDSTACK-WRAPPER: Could not get Job Status (URL error)")
		return json.loads(response)

	# Implementation to be done in the cloudstack
	def recovery_vnf(self,vnf_id):
		request = self.__request_factory('recoveryVnf')
		request['vnfid']=vnf_id
		url = self.__generate_url(request)
		try:
			response = urllib2.urlopen(url).read()
		except Exception as e:
			return (False, "CLOUDSTACK-CLIENT: Could not recovery VNF (URL error)")
		return (True,json.loads(response))

	# Implementation to be done in the cloudstack
	def scale_vnf(self,vnf_id,service_offering_id):
		request = self.__request_factory('scaleVnf')
		request['id']=vnf_id
		request['serviceofferingid']=service_offering_id
		url = self.__generate_url(request)
		try:
			response = urllib2.urlopen(url).read()
		except Exception as e:
			return (False,"CLOUDSTACK-CLIENT: Could not scale VNF (URL error)")
		return (True,json.loads(response))