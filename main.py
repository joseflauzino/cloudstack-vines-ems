#!/usr/bin/env python
import threading
import signal
import logging
from api.api import *
from failure_detector.fd_agent import *
from failure_detector.recovery_agent import *
from auto_scaling.scaling_agent import *
from auto_scaling.mcpa import *

logging.basicConfig(level=logging.INFO, filename='vines_em.log', filemode='w', format='%(levelname)s %(asctime)s - %(message)s')
threads = []

def create_threads():
	threads.append(threading.Thread(target=run_api, name="em-api"))
	threads.append(threading.Thread(target=run_fd_agent, name="em-fd-agent"))
	threads.append(threading.Thread(target=run_recovery_agent, name="em-recovery-agent"))
	threads.append(threading.Thread(target=run_scaling_agent, name="em-scaling-agent"))
	threads.append(threading.Thread(target=run_mcpa, name="em-mcpa"))

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