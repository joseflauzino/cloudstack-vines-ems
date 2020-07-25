#!/usr/bin/env python

import os
import shlex, subprocess

# Runs a shell command, checks for success or error and get command response data
def run_shell_cmd(cmd):
	process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
	output, error = process.communicate()
	if error:
		return {"status":"ERROR","data":error}
	output = output.rstrip("\n")
	if output == "":
		output = "None"
	return {"status":"OK","data":output}


def run_ssh_cmd(cmd):
	process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
	output = process.communicate()
	# TODO: check for success
	if output == "":
		output = "None"
	return {"status":"OK","data":output}