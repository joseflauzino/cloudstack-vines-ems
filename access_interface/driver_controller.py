#!/usr/bin/env python
import os

#==================================================================
#                 Vines - Element Management System
#  Module: Driver Controller                  
#                                                by Jose Flauzino 
#==================================================================

class DriverController():
	"""Driver Controller implementation"""

	# Private methods
	def __init__(self):
		self.drivers = self._import_drivers(self._read_drivers()) # load all drivers

	def _read_drivers(self):
		# TODO: try to allocate all drivers in a specific folder, so that it is not
		# necessary to insert '_driver.py' in the names of the driver files
		drivers_names = []
		for currentFolder, subFolder, files in os.walk("."):
			drivers_names = [os.path.join(file.replace(".py","")) for file in files if file.endswith("_driver.py")]
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
		# instantiate the correct driver and method
		try:
			method = getattr(self._search_driver(self.drivers, self._find_by_key(args,'vnf_platform')), method_name)
		except Exception:
			print "VNF platform driver %s not found"
			return {"status":"ERROR","data":"VNF Platform Driver not found"}
		# call the method
		return method(args)
		# return format {'status':'success or error','data':'the content data'}