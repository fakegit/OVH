# -*- encoding: utf-8 -*-
import sys
import subprocess
import os

'''
###############################################################
#                                                             #
#                    VARIABLES STATIQUES                      #
#															  #
###############################################################
'''

apachePath = "/etc/apache2/apache2.conf"
apacheSitePath = "/etc/apache2/sites-available/000-default.conf"
apacheSiteFile = "<VirtualHost *:80>\n\t\n\tServerAdmin webmaster@localhost\n\tDocumentRoot /var/www/webServer\n\t\n\tErrorLog ${APACHE_LOG_DIR}/error.log\n\tCustomLog ${APACHE_LOG_DIR}/access.log combined\n\t\n</VirtualHost>\n"
apacheModif = "\n<Directory /var/www/webServer/cgi-scripts>\n	Allow from all\n	Options FollowSymLinks\n	Options +ExecCGI\n	AddHandler cgi-script .py\n</Directory>\n"
hostname = subprocess.Popen(["hostname"],stdout=subprocess.PIPE).communicate()[0].decode().split('\n')[0]
setupServerCommands = ["sudo service apache2 restart"]

'''
###############################################################
#                                                             #
#                   CONFIGURATION APACHE2                     #
#															  #
###############################################################
'''

with open(apacheSitePath,"w") as w:
    w.write(apacheSiteFile)

with open(apachePath,"a") as a:
    a.write(apacheModif)

for i in setupServerCommands:
    os.system(i)
