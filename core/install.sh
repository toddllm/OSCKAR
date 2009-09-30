#!/bin/bash

#detect supported platforms
release=`grep DISTRIB_RELEASE /etc/lsb-release  | awk -F\= '{ print $2}'` 
if [ X$release != X9.04 ] && [ X$release != X9.10 ]
then
    echo 'Ubuntu 9.04 and 9.10 are the only fully supported platform at this time'
    exit 1
fi

#install deps
echo -n 'Installing dependencies... '
sudo apt-get install -y qemu ubuntu-virt-mgmt grub

#install deps specific to development and testing
#sudo apt-get install -y nautilus-open-terminal emacs openssh-server denyhosts

#TODO reconfigure ssh server and denyhosts on the fly

echo 'Done'

#patch vmbuilder due to bugs
#echo -n 'Patching vmbuilder (fixing bugs in vmbuilder)... '
#sudo patch -p0 -N < ./patches/vmbuilder.patch
#sudo patch -p0 -N < ./patches/jdstrand.patch
#sudo patch -p0 -N < ./patches/jdstrand2.patch
#echo 'Done'

#install OSCKARcore
echo -n 'Installing OSCKARcore-alpha... '
sudo useradd eventchat -s /bin/sh
sudo useradd policymanager -s /bin/sh
sudo useradd vmminterface -s /bin/sh
sudo useradd builderinterface -s /bin/sh
sudo find . -name '*~' -exec rm {} \;
sudo cp -r ./usr/sbin/* /usr/sbin/
sudo cp -r ./usr/share/* /usr/share/
sudo cp -r ./etc/* /etc/
sudo cp -r ./var/lib/* /var/lib/
sudo cp -r ./var/log/* /var/log/

#access to contracts
sudo chown -R policymanager /var/lib/policymanager

#access to log directories
sudo chown -R eventchat /var/log/eventchat
sudo chown -R policymanager /var/log/policymanager
sudo chown -R vmminterface /var/log/vmminterface
sudo chown -R builderinterface /var/log/builderinterface
echo 'Done'

