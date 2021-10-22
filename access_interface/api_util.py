#! /usr/bin/python3
# description       : API Util
# author            : Jose Flauzino
# email             : jwvflauzino@inf.ufpr.br
# date              : 20211015
# license           : Apache 2.0
# py version        : 3.6.9
#==============================================================================

import subprocess
"""
def run_shell_cmd(cmd_list):
	cmd_response = subprocess.run(cmd_list, stdout=subprocess.PIPE)
	if cmd_response.returncode == 0:
		return {"status":"SUCCESS", "data":cmd_response.stdout}
	return {"status":"ERROR", "data":cmd_response.stdout}
"""

def run_shell_cmd(cmd):
	process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
	output, error = process.communicate()
	if process.returncode != 0:
		print("Command error")
		return {"status":"ERROR","data":output}
	print(output)
	#output = output.rstrip("\n")
	if output == "":
		output = "None"
	return {"status":"SUCCESS","data":output}