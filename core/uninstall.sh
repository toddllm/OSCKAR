#!/bin/bash

sudo rm -rf /etc/init.d/osckar /etc/policymanager/

sudo rm -rf /usr/sbin/eventchat/ /usr/sbin/osckar /usr/sbin/osckar-core-debug /usr/sbin/osckar-interface-builder /usr/sbin/osckar-interface-vmm /usr/sbin/policymanager

sudo rm -rf /usr/share/osckar/

sudo rm -rf /var/lib/osckar/interfaces /var/lib/policymanager

sudo rm -rf /var/log/eventchat /var/log/osckar /var/log/policymanager
sudo rm -rf /var/run/eventchat /var/run/osckar /var/run/policymanager 

echo 'OSCKAR uninstalled.'
echo ''
echo 'NOTE: Any images stored in /var/lib/osckar/images/ will not have been '
echo '      deleted. Remove these files manually if you wish.'
