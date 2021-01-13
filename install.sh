#!/bin/bash

echo "--------------------------------------"
echo " Access Interface installation"
echo "--------------------------------------"
# Install Apache2 Web Server
apt -y update
apt -y install apache2 libapache2-mod-wsgi python-pip

pip install flask requests

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

        WSGIDaemonProcess flaskTest threads=5
        WSGIScriptAlias / /var/www/html/wsgi.py
        <Directory /var/www/html>
           WSGIProcessGroup flaskTest
           WSGIApplicationGroup %{GLOBAL}
           WSGIScriptReloading On
           Require all granted
         </Directory>

        ErrorLog ${APACHE_LOG_DIR}/error.log
        CustomLog ${APACHE_LOG_DIR}/access.log combined

</VirtualHost>
EOM

echo "Restarting Apache2"
systemctl restart apache2

