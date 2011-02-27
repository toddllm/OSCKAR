#!/bin/bash

# Copyright 2010 Todd Deshane <deshantm@gmail.com>
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

sudo rm -rf /etc/init.d/osckar /etc/policymanager/

sudo rm -rf /usr/sbin/eventchat/ /usr/sbin/osckar /usr/sbin/osckar-core-debug /usr/sbin/osckar-interface-builder /usr/sbin/osckar-interface-vmm /usr/sbin/policymanager

sudo rm -rf /usr/share/osckar/

sudo rm -rf /var/lib/osckar/interfaces /var/lib/policymanager

sudo rm -rf /var/log/eventchat /var/log/osckar /var/log/policymanager
sudo rm -rf /var/run/eventchat /var/run/osckar /var/run/policymanager 
sudo userdel eventchat
sudo userdel policymanager
sudo userdel builderinterface
sudo userdel vmminterface

echo 'OSCKAR uninstalled.'
echo ''
echo 'NOTE: Any images stored in /var/lib/osckar/images/ will not have been '
echo '      deleted. Remove these files manually if you wish.'
