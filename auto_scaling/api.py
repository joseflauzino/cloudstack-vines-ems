#!/usr/bin/env python

import json
from eve import Eve
from flask import request, jsonify
from subprocess import Popen, PIPE, check_output, call

app = Eve()

# Add new VNF into list of VNFs to monitor
@app.route('/scaling_agent/add_vnf', methods=['POST'])
def add_vnf():
    vnf_id = request.json['vnf_id']
    vnf_vm_id = request.json['vnf_vm_id']
    vnf_ip = request.json['vnf_ip']
    vnf_name = request.json['vnf_name']
    policy = request.json['policy']
    new_vnf = {'vnf_id':vnf_id,'vnf_vm_id':vnf_vm_id,'vnf_ip':vnf_ip,'vnf_name':vnf_name,'policy':policy}
    monitor = read_file('monitor')
    monitor['vnfs'].append(new_vnf)
    save_file('monitor',monitor)
    return jsonify({'status':'success','data':'Add VNF into monitoring list'})

# Remove VNF of the list of VNFs to monitor
@app.route('/scaling_agent/remove_vnf', methods=['POST'])
def remove_vnf():
    vnf_id = request.json['vnf_id']
    monitor = read_file('monitor')
    i=0
    data = ''
    status = 'success'
    for vnf in monitor['vnfs']:
        if vnf['vnf_id'] == vnf_id:
            try:
                del vnf['vnfs'][i]
                data='Remove VNF of the monitoring list'
            except Exception as e:
                status = "error"
                data = "Could not find VNF in monitoring list: %s" % e
        i+=1
    return jsonify({'status':status,'data': data})

# Update VNF into list of VNFs to monitor
@app.route('/scaling_agent/update_vnf', methods=['POST'])
def update_vnf():
    return jsonify({'data': 'ok'})

# Returns 'Running' if Failure Detector Agent is Ok
@app.route('/scaling_agent/status', methods=['GET'])
def get_status():
    return jsonify({'data': 'Running'})

if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0', port=6000)