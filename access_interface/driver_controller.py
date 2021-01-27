#! /usr/bin/python3
# description       : CloudStack Vines EMS - Driver Controller Module
# author            : Jose Flauzino
# email             : jwvflauzino@inf.ufpr.br
# date              : 20210127
# license           : Apache 2.0
# py version        : 3.6.9
#==============================================================================

import os
import imp
from vib import vib_client

##################################################################
####################### DriverController #########################
##################################################################

class DriverController():

	#------------------------------------------------------------------
	# Private methods
	#------------------------------------------------------------------
	def __init__(self):
		self.drivers_path = os.path.dirname(os.path.realpath(__file__))+"/extended_drivers"
		self.drivers = self._import_drivers(self._read_drivers()) # load all drivers

	def _read_drivers(self):
		drivers_names = []
		for currentFolder, subFolder, files in os.walk(self.drivers_path):
			for file in files:
				if file.endswith("-driver.py"):
					drivers_names.append(file.replace(".py",""))
		return drivers_names

	def _import_drivers(self, drivers_names):
		drivers = []
		for driver in drivers_names:
			drivers.append(imp.load_source(driver, self.drivers_path+"/"+driver+".py"))
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

	#------------------------------------------------------------------
	# Public methods
	#------------------------------------------------------------------
	def handle_call(self, method_name, args):
		vnf_id = self._find_by_key(args,'vnf_id')
		result = vib_client.find_vnf(vnf_id)
		if result["success"] == False:
			return {'status':'error','data':result["data"]}
		args.append({"vnf_ip":result["data"][0]["ip"]})
		args.append({"vnf_platform":result["data"][0]["vnf_exp"]})
		method = getattr(self._search_driver(self.drivers, self._find_by_key(args,'vnf_platform')), method_name)
		return method(args)