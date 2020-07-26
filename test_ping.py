import os
import subprocess

def main():
	print is_vnf_up("192.168.122.1","192.168.122.95")

def is_vnf_up(router_ip, vnf_ip):
    with open(os.devnull, "wb") as limbo:
        #result=subprocess.Popen(["ping", "-c", "1", "-n", "-W", "2", ip],
        #"ssh -i /root/.ssh/id_rsa.cloud %s -p 3922 %s"
        cmd = ["ssh","-i","/root/.ssh/id_rsa.cloud",router_ip,"-p","3922","'ping", "-c", "1", "-n", "-W", "2", vnf_ip,"'"]
        result=subprocess.Popen(cmd,
                stdout=limbo, stderr=limbo).wait()
        if result:
            return False # VNF is crash
        else:
            return True # VNF is up

if __name__ == '__main__':
	main()