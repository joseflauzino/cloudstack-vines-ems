#!/usr/bin/env python

import json
import requests
from eve import Eve
from flask import request, jsonify
from subprocess import Popen, PIPE, check_output, call
from driver_controller import *
from util import *
import sys

#==================================================================
#                 Vines - Element Management System          
#  Module: Access Interface                             
#                                                by Jose Flauzino 
#==================================================================

#------------------------------------------------------------------
# Global definitions
#------------------------------------------------------------------
reload(sys)  
sys.setdefaultencoding('latin1')
app = Eve()
driver_controller = DriverController()

@app.after_request
def after_request(response):
    response.headers.set('Access-Control-Allow-Origin', '*')
    return response

@app.route('/api/ems/status', methods=['GET'])
def ems_status():
    return jsonify({'status':'success','data':'Running'})

#------------------------------------------------------------------
# VNF Lifecycle Management
#------------------------------------------------------------------
@app.route('/api/lifecycle/vnfstatus', methods=['POST'])
def vnf_status():
    args = []
    args.append({"vnf_ip":request.json['vnf_ip']})
    args.append({"router_ip":request.json['router_ip']})
    args.append({"vnf_platform":request.json['vnf_platform']})
    print "args: %s" % args
    response = driver_controller.handle_call("vnf_status",args)
    if response["status"] == "ERROR":
        return {'status':'error','data':"could not get the VNF status"}
    if response["data"] != "Running":
        return {'status':'error','data':"could not get the VNF status"}
    return {'status':'success','data':response["data"]}

@app.route('/api/lifecycle/status', methods=['POST'])
def status():
    args = []
    args.append({"vnf_ip":request.json['vnf_ip']})
    args.append({"router_ip":request.json['router_ip']})
    args.append({"vnf_platform":request.json['vnf_platform']})
    response = driver_controller.handle_call("status",args)
    if response["status"] == "ERROR":
        return {'status':'error','data':"could not get function status"}
    return {'status':'success','data':response["data"]}

@app.route('/api/lifecycle/getlog', methods=['POST'])
def get_log():
    args = []
    args.append(request.json['vnf_ip'])
    args.append(request.json['router_ip'])
    args.append({"vnf_platform":request.json['vnf_platform']})
    response = driver_controller.handle_call("get_log",args)
    if response["status"] == "ERROR":
        return {'status':'error','data':"could not get function log"}
    return {'status':'success','data':response["data"]}

@app.route('/api/lifecycle/stop', methods=['POST'])
def stop_function():
    args = []
    args.append({"vnf_ip":str(request.json['vnf_ip'])})
    args.append({"router_ip":str(request.json['router_ip'])})
    args.append({"vnf_platform":str(request.json['vnf_platform'])})
    response = driver_controller.handle_call("stop",args)
    if response["status"] == "ERROR":
        return {'status':'error','data':"could not stop function"}
    return {'status':'success','data':'Function stopped'}

@app.route('/api/lifecycle/start', methods=['POST'])
def start_function():
    args = []
    args.append({"vnf_ip":str(request.json['vnf_ip'])})
    args.append({"router_ip":str(request.json['router_ip'])})
    args.append({"vnf_platform":str(request.json['vnf_platform'])})
    response = driver_controller.handle_call("start",args)
    if response["status"] == "ERROR":
        return {'status':'error','data':"could not start function"}
    return {'status':'success','data':'Function started'}

@app.route('/api/lifecycle/install', methods=['POST'])
def install():
    args = []
    args.append({"vnf_ip":str(request.json['vnf_ip'])})
    args.append({"router_ip":str(request.json['router_ip'])})
    args.append({"vnf_platform":str(request.json['vnf_platform'])})
    response = driver_controller.handle_call("install",args)
    if response["status"] == "ERROR":
        return {'status':'error','data':"could not install function"}
    return {'status':'success','data':'Function installed'}

@app.route('/api/lifecycle/pushvnfp', methods=['POST'])
def push_vnfp():
    args = []
    args.append({"vnf_ip":str(json.loads(request.form.get('json'))['vnf_ip'])})
    args.append({"router_ip":str(json.loads(request.form.get('json'))['router_ip'])})
    args.append({"vnf_platform":str(json.loads(request.form.get('json'))['vnf_platform'])})
    print args
    f = request.files['file']
    vnfp_path = '/tmp/' + f.filename
    f.save(vnfp_path)
    args.append({"vnfp_path":vnfp_path})
    args.append({"vnfp_filename":f.filename})
    response = driver_controller.handle_call("push_vnfp",args)
    if response["status"] == "ERROR":
        return {'status':'error','data':"could not push VNFP"}
    return {'status':'success','data':'VNFP pushed'}

#------------------------------------------------------------------
# Service Function Chaining
#------------------------------------------------------------------
# VNF configuration
@app.route('/api/sfc/setsfcforwarding', methods=['POST'])
def set_sfc_forwarding():
    args = []
    args.append({"vnf_ip":str(request.json['vnf_ip'])})
    args.append({"router_ip":str(request.json['router_ip'])})
    args.append({"vnf_platform":str(request.json['vnf_platform'])})
    data = request.json['data']
    data = json.dumps(data)
    args.append(data)
    response = driver_controller.handle_call("set_sfc_forwarding",args)
    if response["status"] == "ERROR":
        return {'status':'error','data':"could not configure VNF"}
    return {'status':'success','data':'Forward rule configured'}

# Router configuration
@app.route('/api/sfc/setfirstvnf', methods=['POST'])
def set_first_vnf():
    args = []
    args.append({"vnf_ip":str(request.json['last_vnf'])})
    args.append({"router_ip":str(request.json['first_vnf'])})
    args.append({"router_ip":str(request.json['router_ip'])})
    args.append({"vnf_platform":str(request.json['vnf_platform'])})
    response = driver_controller.handle_call("set_first_vnf",args)
    if response["status"] == "ERROR":
        return {'status':'error','data':"could not set first VNF"}
    return {'status':'success','data':'First VNF route configured'}

def run_api():
    app.run(debug=False,host='0.0.0.0', port=9000)

# remover depois quando for juntar com o resto do codigo
if __name__ == '__main__':
    run_api()

# curl test
# curl -X POST --header "Content-Type: application/json" --data '{"vnf_ip":"192.168.1.100","router_ip":"169.254.0.1","vnf_platform":"vines_leaf_driver"}' http://localhost:9000/api/lifecycle/stop