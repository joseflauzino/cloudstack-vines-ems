#! /usr/bin/python3
# description       : CloudStack Vines EMS - Driver Controller Module
# author            : Jose Flauzino
# email             : jwvflauzino@inf.ufpr.br
# date              : 20210113
# license           : Apache 2.0
# py version        : 3.6.9
#==============================================================================

import os
import sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from vib import vib_client

class DriverController():
	# Private methods
	def __init__(self):
		self.drivers = self._import_drivers(self._read_drivers()) # load all drivers

	def _read_drivers(self):
		# TODO: try to allocate all drivers in a specific folder, so that it is not
		# necessary to insert '_driver.py' in the names of the driver files
		drivers_names = []
		for currentFolder, subFolder, files in os.walk(currentdir):
			print("currentFolder: "+str(currentFolder))
			print("files: "+str(files))
			for file in files:
				if file.endswith("-driver.py"):
					drivers_names.append(file.replace(".py",""))
			#drivers_names = [os.path.join(file.replace(".py","")) for file in files if file.endswith("-driver.py")]
		print("Drivers names: "+str(drivers_names))
		return drivers_names

	def _import_drivers(self, drivers_names):
		drivers = []
		for driver in drivers_names:
			drivers.append(__import__(driver))
		return drivers

	def _search_driver(self, drivers, driver_type):
		for driver in drivers:
			if driver.__name__ == driver_type:
				return driver
		return None

	def _find_by_key(self, array, key):
		for d in array:
			for current_key, current_value in d.items():
				if current_key == key:
					return current_value
		return None

	# Public methods
	def handle_call(self, method_name, args):
		# find VNF in base
		vnf_id = self._find_by_key(args,'vnf_id')
		result = vib_client.find_vnf(vnf_id)
		if result["success"] == False:
			return {'status':'error','data':result["data"]}
		# add VNF data into args
		args.append({"vnf_ip":result["data"][0]["ip"]})
		args.append({"vnf_platform":result["data"][0]["vnf_exp"]})
		# instantiate the correct driver and method
		method = getattr(self._search_driver(self.drivers, self._find_by_key(args,'vnf_platform')), method_name)
		# call the method
		return method(args)