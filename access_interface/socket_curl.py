#!/usr/bin/env python

import os
import sys
import socket

# set of the methods offered by the COVEN platform
valid_methods = ["platform_status","configure","install","start","stop","status","reset","off","close"]


def socket_obj_factory(long_timeout, origin_ip, origin_port, destination_ip, destination_port):
	socketAgent = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	socketAgent.bind((origin_ip, origin_port))
	if long_timeout == True:
		socketAgent.settimeout(10)
	else:
		socketAgent.settimeout(5)
	socketAddr = (destination_ip, destination_port)
	return (socketAddr,socketAgent)


def send_socket_request_with_payload(origin_ip, origin_port, destination_ip, destination_port, method_name, file_path):
	if method_name == "install":
		socketAddr, socketAgent = socket_obj_factory(True, origin_ip, origin_port, destination_ip, destination_port)
		fileName = file_path.replace("\\", "/").split("/")[-1]
		fileSize = os.path.getsize(file_path)
		socketAgent.sendto(("package|" + fileName + "|" + str(fileSize)).encode("utf-8"), socketAddr)
		fileData = open(file_path, "rb")
		fileRead = 0
		while True:
			fileMessage = fileData.read(origin_port)
			socketAgent.sendto(fileMessage, socketAddr)
			fileRead = fileRead + len(fileMessage)
			if fileRead >= fileSize:
				break
		socketAgent.sendto(("install|"+fileName).encode("utf-8"), socketAddr)
		try:
			response, client = socketAgent.recvfrom(origin_port)
		except:
			response = "500|Internal error" # returns a 500 code to represent any server error. TODO: try to get the actual error code
		#sys.exit(response)
		print response
	else: # any method different of 'install' is rejected
		sys.exit(help(1))


def send_socket_request(origin_ip, origin_port, destination_ip, destination_port, method_name):
	socketAddr, socketAgent = socket_obj_factory(False, origin_ip, origin_port, destination_ip, destination_port)
	if method_name not in valid_methods:
		sys.exit(help(1))
	socketAgent.sendto(method_name.encode("utf-8"), socketAddr)
	try:
		response, client = socketAgent.recvfrom(origin_port)
	except:
		response = "500|Internal error" # returns a 500 code to represent any server error. TODO: try to get the actual error code
	#sys.exit(response)
	print response


def help(error_type):
	if error_type == 1: # invalid method name
		print "Invalid method name. Valid values are: %s" % valid_methods
	else: # general invalid usage
		print "USAGE:"
		print "    Simple request"
		print "        Format:  python socket_curl.py <origin_ip> <origin_port> <destination_ip> <destination_port> \"<method_name>\""
		print "        Example: python socket_curl.py 192.168.122.10 1024 10.1.1.101 12345 \"start\""
		print "    Request with payload"
		print "        Format:  python socket_curl.py <origin_ip> <origin_port> <destination_ip> <destination_port> \"<method_name>\" \"zip_file_path\""
		print "        Example: python socket_curl.py 192.168.122.10 1024 10.1.1.101 12345 \"install\" \"/root/vnfp.zip\""	


if __name__=='__main__':
	if len(sys.argv) == 6: # simple request
		send_socket_request(str(sys.argv[1]),int(sys.argv[2]),str(sys.argv[3]),int(sys.argv[4]),str(sys.argv[5]))
	elif len(sys.argv) == 7: # request with payload
		send_socket_request_with_payload(str(sys.argv[1]),int(sys.argv[2]),str(sys.argv[3]),int(sys.argv[4]),str(sys.argv[5]),str(sys.argv[6]))
	else:
		sys.exit(help(0)) # invalid usage