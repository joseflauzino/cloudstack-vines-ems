#!/bin/bash
# description       : CloudStack Vines EMS - Installation Script
# author            : Jose Flauzino
# email             : jwvflauzino@inf.ufpr.br
# date              : 20210127
# license           : Apache 2.0
#==============================================================================

echo "--------------------------------------"
echo " Access Interface installation"
echo "--------------------------------------"
echo "Installing requirements"
apt -y install python3 python3-pip apache2 libapache2-mod-wsgi-py3
pip3 install -r requirements.txt

echo "Creating the Vines EMS directory"
mkdir /etc/cloudstack-vines-ems/
cp -R ./* /etc/cloudstack-vines-ems/
chmod 777 -R /etc/cloudstack-vines-ems/

echo "Creating WSGI configuration file"
cat >/var/www/html/wsgi.py <<'EOM'
import sys
sys.path.insert(0, "/etc/cloudstack-vines-ems/")
from access_interface.api import app as application
EOM

echo "Enabling listening on port 9000"
sed -i -e "s/^Listen 80/Listen 9000/" /etc/apache2/ports.conf

echo "Creating the Virtual Host"
cat >/etc/apache2/sites-available/000-default.conf <<'EOM'
<VirtualHost *:9000>

        ServerAdmin jwvflauzino@inf.ufpr.br
        DocumentRoot /etc/cloudstack-vines-ems/

        WSGIScriptAlias / /var/www/html/wsgi.py
        <Directory /etc/cloudstack-vines-ems/>
           Require all granted
         </Directory>

        ErrorLog ${APACHE_LOG_DIR}/error.log
        CustomLog ${APACHE_LOG_DIR}/access.log combined

</VirtualHost>
EOM

echo "Restarting Apache2"
systemctl restart apache2

echo
echo "--------------------------------------"
echo " Fault Monitor installation"
echo "--------------------------------------"

echo "Creating the Vines EMS Fault Monitor Service"
cat >/lib/systemd/system/vines-ems-fault-monitor.service <<'EOM'
[Unit]
Description=Vines EMS Fault Monitor Service
After=multi-user.target

[Service]
WorkingDirectory=/etc/cloudstack-vines-ems
User=root
Type=idle
ExecStart=/usr/bin/python3 /etc/cloudstack-vines-ems/fault_monitor/fault_monitor.py &> /dev/null
Restart=always

[Install]
WantedBy=multi-user.target
EOM

echo "Reloading deamons"
systemctl daemon-reload
echo "Enabling Fault Monitor"
systemctl enable vines-ems-fault-monitor.service
echo "Starting Fault Monitor"
systemctl start vines-ems-fault-monitor