import requests

def create_url(vnf_ip, task):
    return ''.join(['http://', vnf_ip, ':8000/api/', task])

class ElementManagementClient():
    def __init__(self):
        self.header = {'Content-Type': 'application/json'}
        self.timeout = 5

    def get_metrics(self, vnf_ip):
        """Return usage metrics."""
        url = create_url(vnf_ip, 'metrics')
        return requests.get(url, headers=self.header)