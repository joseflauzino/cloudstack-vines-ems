#!/usr/bin/env python

import urllib2
import urllib
import json
import requests
import subprocess

def create_url(vnf_ip, task):
    return ''.join(['http://', vnf_ip, ':8000/api/', task])

def run_ssh_cmd(cmd):
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output = process.communicate()
    # TODO: check for success
    if output == "":
        output = "None"
    return {"status":"success","data":output}

def send_request(router_ip, url):
    curl_cmd = "'curl -X GET %s'" % (url)
    ssh_cmd = "ssh -i /root/.ssh/id_rsa.cloud %s -p 3922 %s" % (router_ip, curl_cmd)
    response = run_ssh_cmd(ssh_cmd)
    if response["status"] == "error":
        return (False,"Could not get Management Agent response")
    return (True, json.loads(response["data"][0]))

class ManagementAgentClient():
    """Management Agent Client implementation"""

    def __init__(self):
        self.header = {'Content-Type': 'application/json'}
        self.timeout = 5

    def get_emsstatus(self, vnf_ip):
        """Return Management Agent status."""
        return create_url(vnf_ip, 'emsstatus')

    def get_status(self, vnf_ip):
        """Return network function status."""
        return create_url(vnf_ip, 'running')

    def get_log(self, vnf_ip):
        """Return network function log."""
        return create_url(vnf_ip, 'log')

    def get_metrics(self, router_ip, vnf_ip):
        """Return usage metrics."""
        return send_request(router_ip, create_url(vnf_ip, 'metrics'))

    def push_vnfp(self, vnf_ip):
        """Push the VNF Package to VNF VM."""
        return create_url(vnf_ip, 'push_vnfp')

    def stop_function(self, vnf_ip):
        """Stop VNF function."""
        return create_url(vnf_ip, 'stop')

    def start_function(self, vnf_ip):
        """Start VNF function."""
        return create_url(vnf_ip, 'start')

    def install(self, vnf_ip):
        """Install VNF system packages and dependencies."""
        return create_url(vnf_ip, 'install')

    def setsfcforwarding(self, vnf_ip):
        url = create_url(vnf_ip, 'setsfcforwarding')
        return url