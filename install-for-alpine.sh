#!/bin/bash
# description       : CloudStack Vines EMS - Installation Script for Alpine
# author            : Jose Flauzino
# email             : jwvflauzino@inf.ufpr.br
# date              : 20211021
# license           : Apache 2.0
#==============================================================================

echo "Installing requirements"
sed -i -e "s/#h/h/" /etc/apk/repositories
apk update
apk add python3-dev build-base linux-headers pcre-dev py3-pip
pip3 install -r requirements.txt

echo "Creating the Vines EMS directory"
mkdir /etc/cloudstack-vines-ems/
cp -R ./* /etc/cloudstack-vines-ems/

echo "Creating uWSGI configuration file"
cat >/var/www/html/wsgi.py <<'EOM'
import sys
sys.path.insert(0, "/etc/cloudstack-vines-ems/")
from access_interface.api import app
EOM

echo "Configuring autostart"
echo "@reboot uwsgi --socket 0.0.0.0:9000 --protocol=http -w wsgi:app & > /dev/null" >> /etc/crontabs/root