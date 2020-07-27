import os
import subprocess

def main():
        print is_vnf_up("169.254.2.109","10.1.1.249")

def is_vnf_up(router_ip, vnf_ip):
    with open(os.devnull, "wb") as limbo:
        ping_cmd = 'ping -c 1 -n -W 2 %s' % (vnf_ip)
        cmd = 'ssh -i /root/.ssh/id_rsa.cloud %s -p 3922 "%s"' % (router_ip,ping_cmd)
        result = os.system(cmd)
        if result != 0:
            return False # VNF is crash
        else:
            return True # VNF is up

if __name__ == '__main__':
        main()