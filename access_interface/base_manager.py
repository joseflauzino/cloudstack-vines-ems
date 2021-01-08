#!/usr/bin/env python
import os
import json
import uuid

#------------------------------------
# Util
#------------------------------------
def _read_base(base_name):
    base_path = "access_interface/%s.json" % (base_name)
    return json.loads(open(base_path, 'r').read())

def save_base(base_name, data):
    base_path = "access_interface/%s.json" % (base_name)
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
    new_vnf = {"id":find_arg_by_key(args,"vnf_id"),"ip":find_arg_by_key(args,"vnf_ip"),"vnf_exp":find_arg_by_key(args,"vnf_platform")}
    result = find_vnf(new_vnf["id"])
    if result["success"]==True:
        return {"success":False, "data":"Could not add VNF with ID %s: VNF already exists." % (new_vnf["id"])}
    try:
        data = _read_base("vnf_base")
        data["vnfs"].append(new_vnf)
        save_base("vnf_base",data)
    except Exception as e:
        return {"success":False, "data":"Could not add VNF %s: %s" % (new_vnf,e)}
    return {"success":True, "data":new_vnf}

def create_subscription(args):
    new_subscription = {"id":str(uuid.uuid4()),"vnf_id":find_arg_by_key(args,"vnf_id"),"vnfm_ip":find_arg_by_key(args,"vnfm_ip")}
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
    return {"success":True, "data":new_subscription}


#------------------------------------
# READ
#------------------------------------
def find_vnf(vnf_id=None):
    if vnf_id == None:
        try:
            return {"success":True, "data":_read_base("vnf_base")["vnfs"]}
        except Exception as e:
            return {"success":False, "data":"Could not select all VNFs: %s" % (e)}
    data = _read_base("vnf_base")["vnfs"]
    for vnf in data:
        if vnf["id"] == vnf_id:
            return {"success":True, "data":vnf}
    return {"success":False, "data":"Could not find %s" % (vnf_id)}

def find_subscription(subscription_id):
    data = _read_base("subscription_base")["subscriptions"]
    for subscription in data:
        if subscription["id"] == subscription_id:
            return {"success":True, "data":subscription}
    return {"success":False, "data":"Could not find %s" % (subscription_id)}

#------------------------------------
# UPDATE
#------------------------------------
def update_vnf(vnf_id,args):
    data = _read_base("vnf_base")
    for vnf in data["vnfs"]:
        if vnf["id"] == vnf_id:
            for item in args:
                vnf[item.keys()[0]] = item[item.keys()[0]]
            try:
                save_base("vnf_base",data)
            except Exception as e:
                return {"success":False, "data":"Could not update VNF %s: %s" % (vnf,e)}
            return {"success":True, "data":vnf}
    return {"success":False, "data":"Could not find VNF %s to update it" % (vnf_id)}

#------------------------------------
# DELETE
#------------------------------------
def delete_vnf(vnf_id=None):
    if vnf_id == None:
        try:
            data = {"vnfs":[]}
            save_base("vnf_base",data)
        except Exception as e:
            return {"success":False, "data":"Could not remove all VNFs: %s" % (e)}
        return {"success":True, "data":"All VNFs were removed"}
    result = find_vnf(vnf_id)
    if result["success"] == False:
        return result
    vnf = result["data"]
    data = _read_base("vnf_base")
    try:
        data["vnfs"].remove(vnf)
        save_base("vnf_base",data)
    except Exception as e:
        return {"success":False, "data":"Could not remove VNF %s: %s" % (vnf_id,e)}
    return {"success":True, "data":vnf}

def delete_subscription(subscription_id):
    result = find_subscription(subscription_id)
    if result["success"] == False:
        return result
    subscription = result["data"]
    data = _read_base("subscription_base")
    try:
        data["subscriptions"].remove(subscription)
        save_base("subscription_base",data)
    except Exception as e:
        return {"success":False, "data":"Could not remove subscription %s: %s" % (subscription_id,e)}
    return {"success":True, "data":subscription}