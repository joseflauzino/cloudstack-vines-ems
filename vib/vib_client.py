#! /usr/bin/python3
# description       : CloudStack Vines EMS - VIB Module
# author            : Jose Flauzino
# email             : jwvflauzino@inf.ufpr.br
# date              : 20210127
# license           : Apache 2.0
# py version        : 3.6.9
#==============================================================================

import os
import json
import uuid

#------------------------------------
# Util
#------------------------------------
def _read_base(base_name):
    base_path = "%s/%s.json" % (os.path.dirname(os.path.realpath(__file__)),base_name)
    return json.loads(open(base_path, 'r').read())

def save_base(base_name, data):
    base_path = "%s/%s.json" % (os.path.dirname(os.path.realpath(__file__)),base_name)
    open(base_path, 'w+').write(json.dumps(data))

def find_arg_by_key(array, key):
    for d in array:
        for current_key, current_value in d.items():
            if current_key == key:
                return current_value
    return None

#------------------------------------
# CREATE
#------------------------------------
def add_vnf(args):
    new_vnf = {
        "id":find_arg_by_key(args,"vnf_id"),
        "state":"active",
        "ip":find_arg_by_key(args,"vnf_ip"),
        "vnf_exp":find_arg_by_key(args,"vnf_platform")
    }
    result = find_vnf(new_vnf["id"])
    if result["success"]==True:
        return {"success":False, "data":"Could not add VNF with ID %s: VNF already exists." % (new_vnf["id"])}
    try:
        data = _read_base("vnf_base")
        data["vnfs"].append(new_vnf)
        save_base("vnf_base",data)
    except Exception as e:
        return {"success":False, "data":"Could not add VNF %s: %s" % (new_vnf,e)}
    new_vnf["type"]="vnf"
    result = find_arg_by_key(args,"fault_monitoring_policy")
    if result!=None:
        monitoring_interval = result["monitoring_interval"]
        result = add_fault_monitoring_policy(new_vnf["id"],monitoring_interval)
        if result["success"]!=True:
            return {"success":False, "data":"VNF was added, but the fault monitoring policy could not be added"}
        policy = result["data"][0]
        del policy["vnf_id"]
        new_vnf["fault_monitoring_policy"] = policy
    return {"success":True, "data":[new_vnf]}

def add_fault_monitoring_policy(vnf_id,monitoring_interval):
    new_policy = {
        "id":str(uuid.uuid4()),
        "vnf_id":vnf_id,
        "state":"active",
        "monitoring_interval":monitoring_interval
    }
    result = find_policy(new_policy["id"])
    if result["success"]==True:
        return {"success":False, "data":"Could not add policy with ID %s: policy already exists." % (new_policy["id"])}
    try:
        data = _read_base("policy_base")
        data["policies"].append(new_policy)
        save_base("policy_base",data)
    except Exception as e:
        return {"success":False, "data":"Could not add policy %s: %s" % (new_policy,e)}
    new_policy["type"]="policy"
    return {"success":True, "data":[new_policy]}

def create_subscription(args):
    new_subscription = {
        "vnf_id":find_arg_by_key(args,"vnf_id"),
        "vnfm_ip":find_arg_by_key(args,"vnfm_ip"),
        "api_key":find_arg_by_key(args,"api_key"),
        "secret_key":find_arg_by_key(args,"secret_key")
    }
    result = find_vnf(new_subscription["vnf_id"])
    if result["success"]==False:
        return {"success":False, "data":"Could not create the subscription %s: %s" % (new_subscription["id"],result["data"])}
    #TODO: check if this subscription already exists
    try:
        data = _read_base("subscription_base")
        data["subscriptions"].append(new_subscription)
        save_base("subscription_base",data)
    except Exception as e:
        return {"success":False, "data":"Could not create the subscription %s: %s" % (new_subscription,e)}
    new_subscription["type"]="subscription"
    return {"success":True, "data":[new_subscription]}


#------------------------------------
# READ
#------------------------------------
def find_vnf(vnf_id=None):
    if vnf_id == None:
        try:
            vnfs = _read_base("vnf_base")["vnfs"]
            for vnf in vnfs:
                vnf["type"]="vnf"
            return {"success":True, "data":vnfs}
        except Exception as e:
            return {"success":False, "data":"Could not select all VNFs: %s" % (e)}
    data = _read_base("vnf_base")["vnfs"]
    for vnf in data:
        if vnf["id"] == vnf_id:
            vnf["type"]="vnf"
            return {"success":True, "data":[vnf]}
    return {"success":False, "data":"Could not find %s" % (vnf_id)}

def find_policy(vnf_id=None):
    if vnf_id == None:
        try:
            policies = _read_base("policy_base")["policies"]
            return {"success":True, "data":policies}
        except Exception as e:
            return {"success":False, "data":"Could not select all VNFs: %s" % (e)}
    data = _read_base("policy_base")["policies"]
    for policy in data:
        if policy["vnf_id"] == vnf_id:
            policy["type"]="policy"
            return {"success":True, "data":[policy]}
    return {"success":False, "data":"Could not find %s" % (vnf_id)}

def find_subscription(subscription_id):
    data = _read_base("subscription_base")["subscriptions"]
    for subscription in data:
        if subscription["id"] == subscription_id:
            subscription["type"]="subscription"
            return {"success":True, "data":[subscription]}
    return {"success":False, "data":"Could not find %s" % (subscription_id)}

#------------------------------------
# UPDATE
#------------------------------------
def start_vnf_monitoring(args):
    vnf_id = find_arg_by_key(args,"vnf_id")
    data = _read_base("policy_base")
    for policy in data["policies"]:
        if policy["vnf_id"] == vnf_id:
            policy["state"] = "active"
            try:
                save_base("policy_base",data)
            except Exception as e:
                return {"success":False, "data":"Could not start the VNF monitoring."}
            result = find_vnf(vnf_id)
            if result["success"]==False:
                return {"success":False, "data":"Could not start the VNF monitoring: VNF not found."}
            vnf = result["data"][0]
            vnf["fault_monitoring_policy"] = policy
            vnf["type"] = "vnf"
            return {"success":True, "data":[vnf]}
    return {"success":False, "data":"Could not find an monitoring policy related to VNF %s" % (vnf_id)}

def stop_vnf_monitoring(args):
    vnf_id = find_arg_by_key(args,"vnf_id")
    data = _read_base("policy_base")
    for policy in data["policies"]:
        if policy["vnf_id"] == vnf_id:
            policy["state"] = "inactive"
            try:
                save_base("policy_base",data)
            except Exception as e:
                return {"success":False, "data":"Could not stop the VNF monitoring."}
            result = find_vnf(vnf_id)
            if result["success"]==False:
                return {"success":False, "data":"Could not stop the VNF monitoring: VNF not found."}
            vnf = result["data"][0]
            vnf["fault_monitoring_policy"] = policy
            vnf["type"] = "vnf"
            return {"success":True, "data":[vnf]}
    return {"success":False, "data":"Could not find an monitoring policy related to VNF %s" % (vnf_id)}

def update_vnf(vnf_id,args):
    data = _read_base("vnf_base")
    for vnf in data["vnfs"]:
        if vnf["id"] == vnf_id:
            for item in args:
                vnf[list(item.keys())[0]] = item[list(item.keys())[0]]
            try:
                save_base("vnf_base",data)
            except Exception as e:
                return {"success":False, "data":"Could not update VNF %s: %s" % (vnf,e)}
            vnf["type"] = "vnf"
            return {"success":True, "data":[vnf]}
    return {"success":False, "data":"Could not find VNF %s to update it" % (vnf_id)}

#------------------------------------
# DELETE
#------------------------------------
def delete_vnf(vnf_id=None):
    if vnf_id == None:
        try:
            data = {"vnfs":[]}
            save_base("vnf_base",data)
            data = {"policies":[]}
            save_base("policy_base",data)
        except Exception as e:
            return {"success":False, "data":"Could not remove all VNFs: %s" % (e)}
        return {"success":True, "data":[]}
    result = find_vnf(vnf_id)
    if result["success"] == False:
        return result["data"]
    vnf = result["data"][0]
    del vnf["type"] # removing key added by find_vnf() method
    data = _read_base("vnf_base")
    try:
        data["vnfs"].remove(vnf)
        save_base("vnf_base",data)
    except Exception as e:
        return {"success":False, "data":"Could not remove VNF %s: %s" % (vnf_id,e)}
    _delete_policy(vnf["id"])
    return {"success":True, "data":[]}

def _delete_policy(vnf_id):
    result = find_policy(vnf_id)
    if result["success"] == False:
        return result["data"]
    policy = result["data"][0]
    data = _read_base("policy_base")
    try:
        data["policies"].remove(policy)
        save_base("policy_base",data)
    except Exception as e:
        return {"success":False, "data":"Could not remove policy of the VNF %s: %s" % (vnf_id,e)}
    return {"success":True, "data":[]}

def delete_subscription(subscription_id):
    result = find_subscription(subscription_id)
    if result["success"] == False:
        return result
    subscription = result["data"][0]
    del subscription["type"] # removing key added by find_subscription() method
    data = _read_base("subscription_base")
    try:
        data["subscriptions"].remove(subscription)
        save_base("subscription_base",data)
    except Exception as e:
        return {"success":False, "data":"Could not remove subscription %s: %s" % (subscription_id,e)}
    return {"success":True, "data":[]}