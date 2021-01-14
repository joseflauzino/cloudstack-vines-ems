# CloudStack Vines EMS



## Installation

Clone this repository.

	# git clone https://github.com/joseflauzino/cloudstack-vines-em.git

Go to the directory.

	# cd cloudstack-vines-em

Run the install.sh script as root.

	# chmod +x install.sh
	# ./install.sh

## Managing EMS Modules

### Access Interface Module
This module is run by an Apache2 web server using WSGI. So, to managed it uses the apache's systemctl commands.

	# systemctl status apache2  ## get status
	# systemctl stop apache2    ## stop the service
	# systemctl start apache2   ## start the service
	# systemctl restart apache2 ## restart the service

### Fault Monitor
Use the commands bellow to manage this module.

	# systemctl status vines-ems-fault-monitor  ## get status
	# systemctl stop vines-ems-fault-monitor    ## stop the service
	# systemctl start vines-ems-fault-monitor   ## start the service
	# systemctl restart vines-ems-fault-monitor ## restart the service

### Performance Monitor
Use the commands bellow to manage this module.

	# systemctl status vines-ems-perf-monitor  ## get status
	# systemctl stop vines-ems-perf-monitor    ## stop the service
	# systemctl start vines-ems-perf-monitor   ## start the service
	# systemctl restart vines-ems-perf-monitor ## restart the service

## Monitoring EMS Modules Log

### Access Interface Module
Since this module is run by an Apache2 web server using WSGI, the logs are recorded in the Apache2 log files.

Run the command bellow to monitor the access.

	# tail -f /var/log/apache2/access.log

Run the command bellow to monitor errors. 

	# tail -f /var/log/apache2/error.log

