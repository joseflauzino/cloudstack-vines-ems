#!/usr/bin/env python

import os
import sys
import json
import requests
from flask import Flask, request, jsonify
from driver_controller import *
from util import *
import logging

logging.basicConfig(filename='/var/log/apache2/ems.log', level=logging.INFO)
logger = logging.getLogger(__name__)
#==================================================================
#                 Vines - Element Management System          
#  Module: Access Interface                             
#  by Jose Flauzino (jwvflauzino@inf.ufpr.br) 
#==================================================================

##################################################################
###################### Global definitions ########################
##################################################################
reload(sys)  
sys.setdefaultencoding('latin1')
app = Flask(__name__)
driver_controller = DriverController()

@app.after_request
def after_request(response):
    response.headers.set('Access-Control-Allow-Origin', '*')
    return response



##################################################################
########################## EMS Control ###########################
##################################################################

#------------------------------------------------------------------
# EMS
#------------------------------------------------------------------
@app.route('/', methods=['GET'])
def home_page():
    logger.info('This is a INFO log!')
    return os.path.dirname(os.path.realpath(__file__))

@app.route('/v1.0/ems/status', methods=['GET'])
def ems_status():
    return jsonify({'status':'success','data':'Running'})

#------------------------------------------------------------------
# VNF
#------------------------------------------------------------------
@app.route('/v1.0/ems/vnf', methods=['POST','GET','DELETE'])
def ems_vnfs():
    # Register a VNF
    if request.method == 'POST':
        args = []
        args.append({"vnf_id":str(request.json['vnf_id'])})
        args.append({"vnf_ip":str(request.json['vnf_ip'])})
        args.append({"vnf_platform":str(request.json['vnf_platform'])})
        response = add_vnf(args)
        if response["success"] == False:
            return {'status':'error','data':"Could not register the VNF %s" % (response["data"])}
    # Return info about all VNFs
    if request.method == 'GET':
        response = find_vnf()
        if response["success"] == False:
            return {'status':'error','data':response["data"]}
    # Delete all VNFs
    if request.method == 'DELETE':
        response = delete_vnf()
        if response["success"] == False:
            return {'status':'error','data':"Could not delete all VNFs"}
    return {'status':'success','data':response["data"]}

@app.route('/v1.0/ems/vnf/<uuid:vnf_id>', methods=['GET','PUT','DELETE'])
def ems_vnf(vnf_id):
    # Return info about a given VNF
    if request.method == 'GET':
        response = find_vnf(str(vnf_id))
        if response["success"] == False:
            return {'status':'error','data':response["data"]}
    # Update a given VNF
    if request.method == 'PUT':
        args = []
        valid_param_map = [{"vnf_id":"id"},{"vnf_ip":"ip"},{"vnf_platform":"vnf_exp"}]
        at_last_one_param = False
        for param in valid_param_map:
            try:
                external_key = str(param.keys()[0])
                internal_key = str(param[external_key])
                value = str(request.json[external_key])
                args.append({internal_key:value})
                at_last_one_param = True
            except:
                pass #ignore errors
        if at_last_one_param == False:
            return {'status':'error','data':"Could not update the VNF %s. No parameter were given." % (vnf_id)}
        response = update_vnf(str(vnf_id), args)
        if response["success"] == False:
            return {'status':'error','data':"Could not update the VNF %s." % (response["data"])}
    # Delete a VNF
    if request.method == 'DELETE':
        response = delete_vnf(str(vnf_id))
        if response["success"] == False:
            return {'status':'error','data':"Could not delete the VNF %s" % (response["data"])}
    return {'status':'success','data':response["data"]}

# Handle invalid VNF IDs
@app.route('/v1.0/ems/vnf/<string:any_string>', methods=['GET','PUT','DELETE'])
def ems_vnf_invalid_usage_string(any_string):
    return {'status':'error','data':"Invalid usage. The %s value is not a valid UUID." % (any_string)}

@app.route('/v1.0/ems/vnf/<int:any_int>', methods=['GET','PUT','DELETE'])
def ems_vnf_invalid_usage_int(any_int):
    return {'status':'error','data':"Invalid usage. The %s value is not a valid UUID." % (any_int)}

@app.route('/v1.0/ems/vnf/<int:any_float>', methods=['GET','PUT','DELETE'])
def ems_vnf_invalid_usage_float(any_float):
    return {'status':'error','data':"Invalid usage. The %s value is not a valid UUID." % (any_float)}

#------------------------------------------------------------------
# Subscription
#------------------------------------------------------------------
@app.route('/v1.0/ems/subscription', methods=['POST'])
def ems_subscriptions():
    # Create a subscription
    if request.method == 'POST':
        args = []
        args.append({"vnfm_ip":str(request.json['vnfm_ip'])}) # IP of the VNFM (CloudStack Management Server IP)
        args.append({"vnf_id":str(request.json['vnf_id'])}) # ID of the VNF that you want to receive notifications
        response = create_subscription(args)
        if response["success"] == False:
            return {'status':'error','data':response["data"]}
        return {'status':'success','data':response["data"]}

@app.route('/v1.0/ems/subscription/<uuid:subscription_id>', methods=['GET','DELETE'])
def ems_subscription(subscription_id):
    # Return info about a given subscription
    if request.method == 'GET':
        response = find_subscription(str(subscription_id))
        if response["success"] == False:
            return {'status':'error','data':response["data"]}
    # Delete a subscription
    if request.method == 'DELETE':
        response = delete_subscription(str(subscription_id))
        if response["success"] == False:
            return {'status':'error','data':"Could not delete the subscription_id %s" % (response["data"])}
    return {'status':'success','data':response["data"]}

# Handle invalid subscription IDs
@app.route('/v1.0/ems/subscription/<string:any_string>', methods=['GET','PUT','DELETE'])
def ems_subscription_invalid_usage_string(any_string):
    return {'status':'error','data':"Invalid usage. The %s value is not a valid UUID." % (any_string)}

@app.route('/v1.0/ems/subscription/<int:any_int>', methods=['GET','PUT','DELETE'])
def ems_subscription_invalid_usage_int(any_int):
    return {'status':'error','data':"Invalid usage. The %s value is not a valid UUID." % (any_int)}

@app.route('/v1.0/ems/subscription/<int:any_float>', methods=['GET','PUT','DELETE'])
def ems_subscription_invalid_usage_float(any_float):
    return {'status':'error','data':"Invalid usage. The %s value is not a valid UUID." % (any_float)}



##################################################################
################### VNF Lifecycle Management #####################
##################################################################

@app.route('/v1.0/vnf/isup/<uuid:vnf_id>', methods=['GET'])
def vnf_exp_status(vnf_id):
    args = []
    args.append({"vnf_id":str(vnf_id)})
    response = driver_controller.handle_call("vnf_status",args)
    if response["status"] == "ERROR":
        return {'status':'error','data':"Could not get the VNF-ExP status"}
    if response["data"] != "Running":
        return {'status':'error','data':"Could not get the VNF-ExP status"}
    return {'status':'success','data':response["data"]}

@app.route('/v1.0/vnf/status/<uuid:vnf_id>', methods=['GET'])
def status(vnf_id):
    args = []
    args.append({"vnf_id":str(vnf_id)})
    response = driver_controller.handle_call("status",args)
    if response["status"] == "ERROR":
        return {'status':'error','data':"Could not get function status"}
    return {'status':'success','data':response["data"]}

@app.route('/v1.0/vnf/log/<uuid:vnf_id>', methods=['GET'])
def get_log(vnf_id):
    args = []
    args.append({"vnf_id":str(vnf_id)})
    response = driver_controller.handle_call("get_log",args)
    if response["status"] == "ERROR":
        return {'status':'error','data':"Could not get function log"}
    return {'status':'success','data':response["data"]}

@app.route('/v1.0/vnf/stop/<uuid:vnf_id>', methods=['POST'])
def stop_function(vnf_id):
    args = []
    args.append({"vnf_id":str(vnf_id)})
    response = driver_controller.handle_call("stop",args)
    if response["status"] == "ERROR":
        return {'status':'error','data':"Could not stop function"}
    return {'status':'success','data':'Function stopped'}

@app.route('/v1.0/vnf/start/<uuid:vnf_id>', methods=['POST'])
def start_function(vnf_id):
    args = []
    args.append({"vnf_id":str(vnf_id)})
    response = driver_controller.handle_call("start",args)
    if response["status"] == "ERROR":
        return {'status':'error','data':"Could not start function"}
    return {'status':'success','data':'Function started'}

@app.route('/v1.0/vnf/install/<uuid:vnf_id>', methods=['POST'])
def install(vnf_id):
    args = []
    args.append({"vnf_id":str(vnf_id)})
    response = driver_controller.handle_call("install",args)
    if response["status"] == "ERROR":
        return {'status':'error','data':"Could not install function"}
    return {'status':'success','data':'Function installed'}

@app.route('/v1.0/vnf/pushvnfp/<uuid:vnf_id>', methods=['POST'])
def push_vnfp(vnf_id):
    args = []
    args.append({"vnf_id":str(vnf_id)})
    f = request.files['file']
    vnfp_path = '/tmp/' + f.filename
    f.save(vnfp_path)
    args.append({"vnfp_path":vnfp_path})
    args.append({"vnfp_filename":f.filename})
    response = driver_controller.handle_call("push_vnfp",args)
    if response["status"] == "ERROR":
        return {'status':'error','data':"Could not push VNFP"}
    return {'status':'success','data':'VNFP pushed'}

if __name__ == '__main__':
    app.run()