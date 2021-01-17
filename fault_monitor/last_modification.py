import os
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
print(parentdir)
from pathlib import Path

diretorio = Path(parentdir)
arquivo1_name = 'vib/policy_base.json'
arquivo2_name = 'vib/vnf_base.json'

arquivo1 = diretorio/arquivo1_name
arquivo2 = diretorio/arquivo2_name

arquivo1_last_update = arquivo1.stat().st_mtime
arquivo2_last_update = arquivo2.stat().st_mtime

if arquivo1_last_update > arquivo2_last_update:
    print(arquivo1_name+" foi mudado mais recentemente ("+str(arquivo1_last_update)+")")
else:
    print(arquivo2_name+" foi mudado mais recentemente ("+str(arquivo2_last_update)+")")