#!/usr/bin/env python

import json
import requests
from eve import Eve
from flask import request, jsonify
from subprocess import Popen, PIPE, check_output, call
from element_management import *
from util import *
import sys

#==================================================================
#                     Vines Element Management                     
#                                                by Jose Flauzino 
#==================================================================

#------------------------------------------------------------------
# Global definitions
#------------------------------------------------------------------
reload(sys)  
sys.setdefaultencoding('latin1')
app = Eve()
em = ElementManagement()
@app.after_request
def after_request(response):
    response.headers.set('Access-Control-Allow-Origin', '*')
    return response

#------------------------------------------------------------------
# Lifecycle Management
#------------------------------------------------------------------
@app.route('/api/lifecycle/emsstatus', methods=['POST'])
def ems_status():
    vnf_ip = request.json['vnf_ip']
    router_ip = request.json['router_ip']
    http_header = "--header \"Content-Type: application/json\""
    url = em.get_emsstatus(vnf_ip)
    get_emsstatus_cmd = "'curl -X GET %s %s'" % (http_header,url)
    ssh_cmd = "ssh -i /root/.ssh/id_rsa.cloud %s -p 3922 %s" % (router_ip,get_emsstatus_cmd)
    response = run_ssh_cmd(ssh_cmd)
    if response["status"] == "ERROR":
        return {'status':'error','data':"could not get the EMS status"}
    if response["data"][0] != "Running":
        return {'status':'error','data':"could not get the EMS status"}
    return {'status':'success','data':response["data"][0]}

@app.route('/api/gateway/status', methods=['GET'])
def gatewaystatus():
    return jsonify({'status':'success','data':'Running'})

@app.route('/api/lifecycle/get_status', methods=['POST'])
def get_status():
    vnf_ip = request.json['vnf_ip']
    router_ip = request.json['router_ip']
    http_header = "--header \"Content-Type: application/json\""
    url = em.get_status(vnf_ip)
    get_status_cmd = "'curl -X GET %s %s'" % (http_header,url)
    ssh_cmd = "ssh -i /root/.ssh/id_rsa.cloud %s -p 3922 %s" % (router_ip,get_status_cmd)
    response = run_ssh_cmd(ssh_cmd)
    if response["status"] == "ERROR":
        return {'status':'error','data':"could not get function status"}
    return {'status':'success','data':response["data"][0]}

@app.route('/api/lifecycle/get_log', methods=['GET'])
def get_log():
    vnf_ip = request.json['vnf_ip']
    router_ip = request.json['router_ip']
    http_header = "--header \"Content-Type: application/json\""
    url = em.get_log(vnf_ip)
    get_log_cmd = "'curl -X POST %s %s'" % (http_header,url)
    ssh_cmd = "ssh -i /root/.ssh/id_rsa.cloud %s -p 3922 %s" % (router_ip,get_log_cmd)
    response = run_ssh_cmd(ssh_cmd)
    if response["status"] == "ERROR":
        return {'status':'error','data':"could not get function log"}
    return {'status':'success','data':response["data"][0]}

@app.route('/api/lifecycle/stop_function', methods=['POST'])
def stop_function():
    vnf_ip = request.json['vnf_ip']
    router_ip = request.json['router_ip']
    http_header = "--header \"Content-Type: application/json\""
    url = em.stop_function(vnf_ip)
    stop_cmd = "'curl -X POST %s %s'" % (http_header,url)
    ssh_cmd = "ssh -i /root/.ssh/id_rsa.cloud %s -p 3922 %s" % (router_ip,stop_cmd)
    response = run_ssh_cmd(ssh_cmd)
    if response["status"] == "ERROR":
        print "ERRO: %s" % response["data"]
        return {'status':'error','data':"could not stop function"}
    return {'status':'success','data':'Function stopped'}

@app.route('/api/lifecycle/start_function', methods=['POST'])
def start_function():
    vnf_ip = request.json['vnf_ip']
    router_ip = request.json['router_ip']
    http_header = "--header \"Content-Type: application/json\""
    url = em.start_function(vnf_ip)
    start_cmd = "'curl -X POST %s %s'" % (http_header,url)
    ssh_cmd = "ssh -i /root/.ssh/id_rsa.cloud %s -p 3922 %s" % (router_ip,start_cmd)
    response = run_ssh_cmd(ssh_cmd)
    if response["status"] == "ERROR":
        print "ERRO: %s" % response["data"]
        return {'status':'error','data':"could not start function"}
    return {'status':'success','data':'Function started'}

@app.route('/api/lifecycle/install', methods=['POST'])
def install():
    vnf_ip = request.json['vnf_ip']
    router_ip = request.json['router_ip']
    http_header = "--header \"Content-Type: application/json\""
    url = em.install(vnf_ip)
    install_cmd = "'curl -X POST %s %s'" % (http_header,url)
    ssh_cmd = "ssh -i /root/.ssh/id_rsa.cloud %s -p 3922 %s" % (router_ip,install_cmd)
    response = run_ssh_cmd(ssh_cmd)
    if response["status"] == "ERROR":
        print "ERRO: %s" % response["data"]
        return {'status':'error','data':"could not install function"}
    return {'status':'success','data':'Function installed'}

@app.route('/api/lifecycle/push_vnfp', methods=['POST'])
def push_vnfp():
    vnf_ip = json.loads(request.form.get('json'))['vnf_ip']
    router_ip = json.loads(request.form.get('json'))['router_ip']
    f = request.files['file']
    function_path = '/tmp/' + f.filename
    f.save(function_path)
    http_header = "--header \"Content-Type: application/zip\""
    url = em.push_vnfp(vnf_ip)
    # Send VNFP file to router via SCP
    scp_cmd = "scp -i /root/.ssh/id_rsa.cloud -P 3922 %s root@%s:/root/" % (function_path,router_ip)
    response = run_ssh_cmd(scp_cmd)
    if response["status"] == "ERROR":
        return jsonify({'function': None})
    # Send SSH command to router.
    # VNFP file from router to VNF via HTTP (curl command)
    curlCmd = "'curl -i -X POST %s --data-binary @/root/%s %s'" % (http_header,f.filename, url)
    ssh_cmd = "ssh -i /root/.ssh/id_rsa.cloud %s -p 3922 %s" % (router_ip,curlCmd)
    response = run_ssh_cmd(ssh_cmd)
    if response["status"] == "ERROR":
        return {'status':'error','data':"could not push VNFP"}
    return {'status':'success','data':'VNFP pushed'}

#------------------------------------------------------------------
# Service Function Chaining
#------------------------------------------------------------------
# VNF
@app.route('/api/sfc/setsfcforwarding', methods=['POST'])
def setsfcforwarding():
    router_ip = request.json['router_ip']
    vnf_ip = request.json['vnf_ip']
    data = request.json['data']
    data = json.dumps(data)
    http_header = "--header \"Content-Type: application/json\""
    url = em.setsfcforwarding(vnf_ip)
    set_sfc_forwarding_cmd = "'curl -X POST %s --data' \"'\" '%s' \"'\" '%s'" % (http_header,data,url)
    ssh_cmd = "ssh -i /root/.ssh/id_rsa.cloud %s -p 3922 %s" % (router_ip,set_sfc_forwarding_cmd)
    response = run_ssh_cmd(ssh_cmd)
    if response["status"] == "ERROR":
        return {'status':'error','data':"could not configure VNF"}
    return {'status':'success','data':'Forward rule configured'}

# Router
@app.route('/api/sfc/setfirstvnf', methods=['POST'])
def setfirstvnf():
    last_vnf = request.json['last_vnf']
    first_vnf = request.json['first_vnf']
    router_ip = request.json['router_ip']
    set_first_vnf_cmd = "ip route add %s via %s" % (last_vnf,first_vnf)
    ssh_cmd = 'ssh -i /root/.ssh/id_rsa.cloud %s -p 3922 \'%s\'' % (router_ip,set_first_vnf_cmd)
    response = run_ssh_cmd(ssh_cmd)
    if response["status"] == "ERROR":
        return {'status':'error','data':"could not set first VNF"}
    return {'status':'success','data':'First VNF route configured'}
"""
#------------------------------------------------------------------
# Failure Detector
#------------------------------------------------------------------
@app.route('/fd/add_vnf', methods=['POST'])
def add_vnf():
    vnf_vm_id = request.json['vnf_vm_id']
    vnf_ip = request.json['vnf_ip']
    vnf_name = request.json['vnf_name']
    new_vnf = {'vnf_vm_id':vnf_vm_id,'vnf_ip':vnf_ip,'vnf_name':vnf_name,'timeouts':0}
    alive = json.loads(open('alive', 'r').read())
    alive['vnfs'].append(new_vnf)
    open('alive', 'w+').write(json.dumps(alive))
    return jsonify({'data': cs.test()})

# Remove VNF of the list of VNFs to monitor
@app.route('/fd/remove_vnf', methods=['POST'])
def remove_vnf():
    return jsonify({'data': 'ok'})

# Update VNF into list of VNFs to monitor
@app.route('/fd/update_vnf', methods=['POST'])
def update_vnf():
    return jsonify({'data': 'ok'})

# Returns 'Running' if Failure Detector Agent is Ok
@app.route('/fd/status', methods=['GET'])
def get_status():
    return jsonify({'data': 'Running'})

#------------------------------------------------------------------
# Auto Scaling
#------------------------------------------------------------------
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
"""
def run_api():
    app.run(debug=False,host='0.0.0.0', port=9000)