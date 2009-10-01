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


#make installable/clean distribution of osckar
mkdir -p ./dist/usr/sbin/
mkdir -p ./dist/usr/share/
mkdir -p ./dist/etc/
mkdir -p ./dist/var/lib/
mkdir -p ./dist/var/log/
mkdir -p ./dist/var/run/

sudo cp -rp ./usr/sbin/* ./dist/usr/sbin/
sudo cp -rp ./usr/share/* ./dist/usr/share/
sudo cp -rp ./etc/* ./dist/etc/
sudo cp -rp ./var/lib/* ./dist/var/lib/
sudo cp -rp ./var/log/* ./dist/var/log/
sudo cp -rp ./var/run/* ./dist/var/run/

#clean dist
sudo find ./dist/ -name '*~' -exec rm {} \;
find ./dist/ -name '.svn' -exec rm -rf {} \; > /dev/null 2>&1

#install from dist
sudo cp -rp ./dist/usr/sbin/* /usr/sbin/
sudo cp -rp ./dist/usr/share/* /usr/share/
sudo cp -rp ./dist/etc/* /etc/
sudo cp -rp ./dist/var/lib/* /var/lib/
sudo cp -rp ./dist/var/log/* /var/log/
sudo cp -rp ./dist/var/log/* /var/run/

#access to contracts
sudo chown -R policymanager /var/lib/policymanager
sudo chown -R vmminterface /var/lib/osckar/interfaces/vmm

#access to log directories
sudo chown -R eventchat /var/log/eventchat
sudo chown -R policymanager /var/log/policymanager
sudo chown -R vmminterface /var/log/vmminterface
sudo chown -R builderinterface /var/log/builderinterface

#access to (/var/run) pid directories
sudo chown -R eventchat /var/run/eventchat
sudo chown -R policymanager /var/run/policymanager
sudo chown -R vmminterface /var/run/vmminterface
sudo chown -R builderinterface /var/run/builderinterface
echo 'Done'

