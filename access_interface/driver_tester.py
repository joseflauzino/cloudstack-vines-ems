#!/usr/bin/env python

module = __import__("click-on-osv-driver")

args = [{'vnf_ip':'192.168.122.127'}]

print module.push_vnfp(args)