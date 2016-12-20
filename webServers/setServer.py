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
apacheModif = "<Directory /var/www/html/cgi-scripts>\n	Allow from all\n	Options FollowSymLinks\n	Options +ExecCGI\n	AddHandler cgi-script .py\n</Directory>"
hostname = subprocess.Popen(["hostname"],stdout=subprocess.PIPE).communicate()[0].decode().split('\n')[0]
setupServerCommands = ["ssh root@{0} apt-get apache2" , "ssh root@{0} sudo service apache2 restart"]

'''
###############################################################
#                                                             #
#                   CONFIGURATION APACHE2                     #
#															  #
###############################################################
'''

with open(apachePath,"a") as a:
a.write(apacheModif)

for i in setupServerCommands:
    os.system(i.format(hostname))
