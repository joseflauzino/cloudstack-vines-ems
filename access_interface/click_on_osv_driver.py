#!/usr/bin/env python

def install(args):
	response = "Executando install com o driver click-on-osv"
	print args
	print response
	return {'status':'success','data':response}

def start(args):
	response = "Executando start com o driver click-on-osv"
	print args
	print response
	return {'status':'success','data':response}

def stop(args):
	response = "Executando stop com o driver click-on-osv"
	print args
	print response
	return {'status':'success','data':response}