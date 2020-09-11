#!/usr/bin/env python

module = __import__("coven-driver")

args = [
		{'vnf_ip':'192.168.122.225'},
		{'router_ip':'192.168.122.1'},
		{'vnfp_path':'/home/jwvflauzino/Research/Dissertacao/coven/COVEN/COVEN-Forwarder.zip'}
	]

print module.push_vnfp(args)