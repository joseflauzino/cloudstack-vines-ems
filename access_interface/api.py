#! /usr/bin/python3
# description       : CloudStack Vines EMS - Access Interface Module
# author            : Jose Flauzino
# email             : jwvflauzino@inf.ufpr.br
# date              : 20211015
# license           : Apache 2.0
# py version        : 3.6.9
#==============================================================================

import os
import sys
import json
from flask import Flask, request
from access_interface.driver_controller import *
from access_interface.api_util import *

##################################################################
###################### Global definitions ########################
##################################################################

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
@app.route('/v1.0/ems/status', methods=['GET'])
def ems_status():
    return {'status':'success','message':'Running'}

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

        if request.json.get('fault_monitoring_policy'): # there is a fault monitoring policy
            args.append({"fault_monitoring_policy":request.json['fault_monitoring_policy']})

        response = vib_client.add_vnf(args)
        if response["success"] == False:
            return {'status':'error','message':response["data"]}
        return {'status':'success','message':'VNF successfully registred','object':response["data"]}
    # Return info about all VNFs
    if request.method == 'GET':
        response = vib_client.find_vnf()
        if response["success"] == False:
            return {'status':'error','message':response["data"]}
        return {'status':'success','message':'VNFs successfully getted','object':response["data"]}
    # Delete all VNFs
    if request.method == 'DELETE':
        response = vib_client.delete_vnf()
        if response["success"] == False:
            return {'status':'error','message':response["data"]}
        return {'status':'success','message':'VNFs successfully deleted','object':response["data"]}

@app.route('/v1.0/ems/vnf/<uuid:vnf_id>', methods=['GET','PATCH','DELETE'])
def ems_vnf(vnf_id):
    # Return info about a given VNF
    if request.method == 'GET':
        response = vib_client.find_vnf(str(vnf_id))
        if response["success"] == False:
            return {'status':'error','message':response["data"]}
        return {'status':'success','message':'VNF successfully getted','object':response["data"]}
    # Update a given VNF
    if request.method == 'PATCH':
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
            return {'status':'error','message':"Could not update the VNF "+vnf_id+". No parameter were given."}
        response = vib_client.update_vnf(str(vnf_id), args)
        if response["success"] == False:
            return {'status':'error','message':response["data"]}
        return {'status':'success','message':'VNF successfully updated','object':response["data"]}
    # Delete a VNF
    if request.method == 'DELETE':
        response = vib_client.delete_vnf(str(vnf_id))
        if response["success"] == False:
            return {'status':'error','message':response["data"]}
        return {'status':'success','message':'VNF successfully deleted','object':response["data"]}

# Handle invalid VNF IDs
@app.route('/v1.0/ems/vnf/<string:invalid_value>', methods=['GET','PATCH','DELETE'])
def ems_vnf_invalid_usage_string(invalid_value):
    return invaliUuidResponse(invalid_value)

@app.route('/v1.0/ems/vnf/<int:invalid_value>', methods=['GET','PATCH','DELETE'])
def ems_vnf_invalid_usage_int(invalid_value):
    return invaliUuidResponse(invalid_value)

@app.route('/v1.0/ems/vnf/<float:invalid_value>', methods=['GET','PATCH','DELETE'])
def ems_vnf_invalid_usage_float(invalid_value):
    return invaliUuidResponse(invalid_value)

@app.route('/v1.0/ems/vnf/startmonitoring/<uuid:vnf_id>', methods=['POST'])
def ems_vnf_start_monitoring(vnf_id):
    print("Start monitoring")
    args = []
    args.append({"vnf_id":str(vnf_id)})
    response = vib_client.start_vnf_monitoring(args)
    if response["success"] == False:
        return {'status':'error','message':response["data"]}
    return {'status':'success','message':'VNF monitoring was successfully started','object':response["data"]}

@app.route('/v1.0/ems/vnf/stopmonitoring/<uuid:vnf_id>', methods=['POST'])
def ems_vnf_stop_monitoring(vnf_id):
    args = []
    args.append({"vnf_id":str(vnf_id)})
    response = vib_client.stop_vnf_monitoring(args)
    if response["success"] == False:
        return {'status':'error','message':response["data"]}
    return {'status':'success','message':'VNF monitoring was successfully stop','object':response["data"]}

# Handle invalid VNF IDs
@app.route('/v1.0/ems/vnf/startmonitoring/<string:invalid_value>', methods=['POST'])
def ems_vnf_start_monitoring_invalid_usage_string(invalid_value):
    return invaliUuidResponse(invalid_value)

@app.route('/v1.0/ems/vnf/startmonitoring/<int:invalid_value>', methods=['POST'])
def ems_vnf_start_monitoring_invalid_usage_int(invalid_value):
    return invaliUuidResponse(invalid_value)

@app.route('/v1.0/ems/vnf/startmonitoring/<float:invalid_value>', methods=['POST'])
def ems_vnf_start_monitoring_invalid_usage_float(invalid_value):
    return invaliUuidResponse(invalid_value)

@app.route('/v1.0/ems/vnf/stopmonitoring/<string:invalid_value>', methods=['POST'])
def ems_vnf_stop_monitoring_invalid_usage_string(invalid_value):
    return invaliUuidResponse(invalid_value)

@app.route('/v1.0/ems/vnf/stopmonitoring/<int:invalid_value>', methods=['POST'])
def ems_vnf_stop_monitoring_invalid_usage_int(invalid_value):
    return invaliUuidResponse(invalid_value)

@app.route('/v1.0/ems/vnf/stopmonitoring/<float:invalid_value>', methods=['POST'])
def ems_vnf_stop_monitoring_invalid_usage_float(invalid_value):
    return invaliUuidResponse(invalid_value)

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
        args.append({"api_key":str(request.json['api_key'])}) # the API Key that will be used to notify the VNFM
        args.append({"secret_key":str(request.json['secret_key'])}) # the Secret Key that will be used to notify the VNFM
        response = vib_client.create_subscription(args)
        if response["success"] == False:
            return {'status':'error','message':response["data"]}
        return {'status':'success','message':response["data"]}

@app.route('/v1.0/ems/subscription/<uuid:subscription_id>', methods=['GET','DELETE'])
def ems_subscription(subscription_id):
    # Return info about a given subscription
    if request.method == 'GET':
        response = vib_client.find_subscription(str(subscription_id))
        if response["success"] == False:
            return {'status':'error','message':response["data"]}
    # Delete a subscription
    if request.method == 'DELETE':
        response = vib_client.delete_subscription(str(subscription_id))
        if response["success"] == False:
            return {'status':'error','message':response["data"]}
    return {'status':'success','message':response["data"]}

# Handle invalid subscription IDs
@app.route('/v1.0/ems/subscription/<string:invalid_value>', methods=['GET','PATCH','DELETE'])
def ems_subscription_invalid_usage_string(invalid_value):
    return invaliUuidResponse(invalid_value)

@app.route('/v1.0/ems/subscription/<int:invalid_value>', methods=['GET','PATCH','DELETE'])
def ems_subscription_invalid_usage_int(invalid_value):
    return invaliUuidResponse(invalid_value)

@app.route('/v1.0/ems/subscription/<float:invalid_value>', methods=['GET','PATCH','DELETE'])
def ems_subscription_invalid_usage_float(invalid_value):
    return invaliUuidResponse(invalid_value)



##################################################################
################### VNF Lifecycle Management #####################
##################################################################

#------------------------------------------------------------------
# Is up?
#------------------------------------------------------------------
@app.route('/v1.0/vnf/isup/<uuid:vnf_id>', methods=['GET'])
def vnf_exp_status(vnf_id):
    args = []
    args.append({"vnf_id":str(vnf_id)})
    response = driver_controller.handle_call("vnf_status",args)
    if response["status"] == "ERROR":
        return {'status':'error','message':"Could not get the VNF-ExP status"}
    if response["data"] != "Running":
        return {'status':'error','message':"Could not get the VNF-ExP status"}
    return {'status':'success','message':response["data"]}

@app.route('/v1.0/vnf/isup/<string:invalid_value>', methods=['GET'])
def vnf_exp_status_invalid_usage_string(invalid_value):
    return invaliUuidResponse(invalid_value)

@app.route('/v1.0/vnf/isup/<int:invalid_value>', methods=['GET'])
def vnf_exp_status_invalid_usage_int(invalid_value):
    return invaliUuidResponse(invalid_value)

@app.route('/v1.0/vnf/isup/<float:invalid_value>', methods=['GET'])
def vnf_exp_status_invalid_usage_float(invalid_value):
    return invaliUuidResponse(invalid_value)

#------------------------------------------------------------------
# Push VNF Package
#------------------------------------------------------------------
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
        return {'status':'error','message':"Could not push VNFP"}
    return {'status':'success','message':'VNFP pushed'}

@app.route('/v1.0/vnf/pushvnfp/<string:invalid_value>', methods=['POST'])
def push_vnfp_invalid_usage_string(invalid_value):
    return invaliUuidResponse(invalid_value)

@app.route('/v1.0/vnf/pushvnfp/<int:invalid_value>', methods=['POST'])
def push_vnfp_invalid_usage_int(invalid_value):
    return invaliUuidResponse(invalid_value)

@app.route('/v1.0/vnf/pushvnfp/<float:invalid_value>', methods=['POST'])
def push_vnfp_invalid_usage_float(invalid_value):
    return invaliUuidResponse(invalid_value)

#------------------------------------------------------------------
# Install
#------------------------------------------------------------------
@app.route('/v1.0/vnf/install/<uuid:vnf_id>', methods=['POST'])
def install(vnf_id):
    args = []
    args.append({"vnf_id":str(vnf_id)})
    response = driver_controller.handle_call("install",args)
    if response["status"] == "ERROR":
        return {'status':'error','message':"Could not install function"}
    return {'status':'success','message':'Function installed'}

@app.route('/v1.0/vnf/install/<string:invalid_value>', methods=['POST'])
def install_invalid_usage_string(invalid_value):
    return invaliUuidResponse(invalid_value)

@app.route('/v1.0/vnf/install/<int:invalid_value>', methods=['POST'])
def install_invalid_usage_int(invalid_value):
    return invaliUuidResponse(invalid_value)

@app.route('/v1.0/vnf/install/<float:invalid_value>', methods=['POST'])
def install_invalid_usage_float(invalid_value):
    return invaliUuidResponse(invalid_value)

#------------------------------------------------------------------
# Start
#------------------------------------------------------------------
@app.route('/v1.0/vnf/start/<uuid:vnf_id>', methods=['POST'])
def start_function(vnf_id):
    args = []
    args.append({"vnf_id":str(vnf_id)})
    response = driver_controller.handle_call("start",args)
    if response["status"] == "ERROR":
        return {'status':'error','message':"Could not start function"}
    return {'status':'success','message':'Function started'}

@app.route('/v1.0/vnf/start/<string:invalid_value>', methods=['POST'])
def start_function_invalid_usage_string(invalid_value):
    return invaliUuidResponse(invalid_value)

@app.route('/v1.0/vnf/start/<int:invalid_value>', methods=['POST'])
def start_function_invalid_usage_int(invalid_value):
    return invaliUuidResponse(invalid_value)

@app.route('/v1.0/vnf/start/<float:invalid_value>', methods=['POST'])
def start_function_invalid_usage_float(invalid_value):
    return invaliUuidResponse(invalid_value)

#------------------------------------------------------------------
# Stop
#------------------------------------------------------------------
@app.route('/v1.0/vnf/stop/<uuid:vnf_id>', methods=['POST'])
def stop_function(vnf_id):
    args = []
    args.append({"vnf_id":str(vnf_id)})
    response = driver_controller.handle_call("stop",args)
    if response["status"] == "ERROR":
        return {'status':'error','message':"Could not stop function"}
    return {'status':'success','message':'Function stopped'}

@app.route('/v1.0/vnf/stop/<string:invalid_value>', methods=['POST'])
def stop_function_invalid_usage_string(invalid_value):
    return invaliUuidResponse(invalid_value)

@app.route('/v1.0/vnf/stop/<int:invalid_value>', methods=['POST'])
def stop_function_invalid_usage_int(invalid_value):
    return invaliUuidResponse(invalid_value)

@app.route('/v1.0/vnf/stop/<float:invalid_value>', methods=['POST'])
def stop_function_invalid_usage_float(invalid_value):
    return invaliUuidResponse(invalid_value)

#------------------------------------------------------------------
# Status
#------------------------------------------------------------------
@app.route('/v1.0/vnf/status/<uuid:vnf_id>', methods=['GET'])
def status(vnf_id):
    args = []
    args.append({"vnf_id":str(vnf_id)})
    response = driver_controller.handle_call("status",args)
    if response["status"] == "ERROR":
        return {'status':'error','message':"Could not get function status"}
    return {'status':'success','message':response["data"]}

@app.route('/v1.0/vnf/status/<string:invalid_value>', methods=['GET'])
def status_invalid_usage_string(invalid_value):
    return invaliUuidResponse(invalid_value)

@app.route('/v1.0/vnf/status/<int:invalid_value>', methods=['GET'])
def status_invalid_usage_int(invalid_value):
    return invaliUuidResponse(invalid_value)

@app.route('/v1.0/vnf/status/<float:invalid_value>', methods=['GET'])
def status_invalid_usage_float(invalid_value):
    return invaliUuidResponse(invalid_value)


##################################################################
############################ Common ##############################
##################################################################

def invaliUuidResponse(invalid_value):
    return {'status':'error','message':"Invalid usage. The "+invalid_value+" value is not a valid UUID."}



##################################################################
################# Service Function Chaining ######################
##################################################################

#------------------------------------------------------------------
# SFC configuration
#------------------------------------------------------------------
@app.route('/v1.0/sfc/setsfcforwarding', methods=['POST'])
def setsfcforwarding():
    args = []
    args.append({"vnf_ip":str(request.json['vnf_ip'])})
    args.append({"data":str(json.dumps(request.json['data']))})
    response = driver_controller.handle_call("set_sfc_forwarding",args)
    if response["status"] == "ERROR":
        return {'status':'error','message':"Could not set SFC forwarding"}
    return {'status':'success','message':'Forward rule configured'}

@app.route('/api/sfc/setfirstvnf', methods=['POST'])
def setfirstvnf():
    set_first_vnf_cmd = "ip route add %s via %s" % (request.json['last_vnf'], request.json['first_vnf'])
    ssh_cmd = 'ssh -i /root/.ssh/id_rsa.cloud %s -p 3922 \'%s\'' % (request.json['router_ip'], set_first_vnf_cmd)
    response = run_shell_cmd(ssh_cmd)
    if response["status"] == "ERROR":
        return {'status':'error','data':"could not set first VNF"}
    return {'status':'success','data':'First VNF route configured'}
"""
def setfirstvnf():
    set_first_vnf_cmd = "ip route add %s via %s" % (request.json['last_vnf'], request.json['first_vnf'])
    ssh_cmd = 'ssh -i /root/.ssh/id_rsa.cloud %s -p 3922 \'%s\'' % (request.json['router_ip'], set_first_vnf_cmd)
    cmd_list = []
    for part in ssh_cmd.split(' '):
        cmd_list.append(part)
    response = run_shell_cmd(cmd_list)
    if response["status"] == "ERROR":
        return {'status':'error','data':"could not set first VNF"}
    return {'status':'success','data':'First VNF route configured'}
"""


##################################################################
############################# Main ###############################
##################################################################
if __name__ == '__main__':
    app.run()