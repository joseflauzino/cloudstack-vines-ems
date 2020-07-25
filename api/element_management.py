#!/usr/bin/env python

import requests

def create_url(vnf_ip, task):
    return ''.join(['http://', vnf_ip, ':8000/api/', task])

class ElementManagement():
    """Implementation of the Element Management System (EMS)."""

    def __init__(self):
        self.header = {'Content-Type': 'application/json'}
        self.timeout = 5

    def get_emsstatus(self, vnf_ip):
        """Return EMS status."""
        return create_url(vnf_ip, 'emsstatus')

    def get_status(self, vnf_ip):
        """Return function status."""
        return create_url(vnf_ip, 'running')

    def get_log(self, vnf_ip):
        """Return function log."""
        return create_url(vnf_ip, 'log')

    def get_metrics(self, vnf_ip):
        """Return usage metrics."""
        return create_url(vnf_ip, 'metrics')

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