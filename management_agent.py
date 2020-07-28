#!/usr/bin/env python

import urllib2
import urllib
import json
import requests

def create_url(vnf_ip, task):
    return ''.join(['http://', vnf_ip, ':8000/api/', task])

def send_request(url):
        try:
            response=urllib2.urlopen(url)
        except:
            return (False, "URL error")
        return (True, json.loads(response.read()))

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

    def get_metrics(self, vnf_ip):
        """Return usage metrics."""
        return send_request(create_url(vnf_ip, 'metrics'))

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