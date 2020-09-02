#!/usr/bin/env python
import threading
import signal
import logging
from access_interfce.api import *
from fault_monitor.fd_agent import *
from fault_monitor.recovery_agent import *
from perf_monitor.scaling_agent import *
from perf_monitor.mcpa import *

logging.basicConfig(level=logging.INFO, filename='vines_em.log', filemode='w', format='%(levelname)s %(asctime)s - %(message)s')
threads = []

def create_threads():
	threads.append(threading.Thread(target=run_api, name="ems-access-interface"))
	#threads.append(threading.Thread(target=run_fd_agent, name="ems-fault-monitor"))
	#threads.append(threading.Thread(target=run_recovery_agent, name="ems-recovery-agent"))
	#threads.append(threading.Thread(target=run_scaling_agent, name="ems-scaling-agent"))
	#threads.append(threading.Thread(target=run_mcpa, name="em-mcpa"))

def stop_threads():
	print "Stopping the EM"
	os.kill(os.getpid(), signal.SIGTERM)

def main():
	create_threads()
	for i in threads:
		i.start()
	while True:
		time.sleep(1)

if __name__ == '__main__':
	try:
		logging.info('Vines EM is running')
		main()
	except (KeyboardInterrupt):
		stop_threads()