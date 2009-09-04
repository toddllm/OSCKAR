#!/bin/bash

#detect supported platforms
release=`grep DISTRIB_RELEASE /etc/lsb-release  | awk -F\= '{ print $2}'` 
if [ X$release != X9.04 ]
then
    echo 'Ubuntu 9.04 is the only fully supported platform at this time'
    exit 1
fi

#install deps
echo -n 'Installing dependencies... '
sudo apt-get install -y qemu ubuntu-virt-mgmt 

#install deps specific to development and testing
sudo apt-get install -y nautilus-open-terminal emacs openssh-server denyhosts

#TODO reconfigure ssh server and denyhosts on the fly

echo 'Done'

#patch vmbuilder due to bugs
echo -n 'Patching vmbuilder (fixing bugs in vmbuilder)... '
sudo patch -p0 -N < ./patches/vmbuilder.patch
sudo patch -p0 -N < ./patches/jdstrand.patch
sudo patch -p0 -N < ./patches/jdstrand2.patch
echo 'Done'

#install OSCARcore
echo -n 'Installing OSCARcore-dev... '
sudo find . -name '*~' -exec rm {} \;
sudo cp -r ./usr/local/bin/* /usr/local/bin/
sudo cp -r ./usr/local/share/* /usr/local/share/
sudo cp -r ./etc/* /etc/
sudo mkdir -p /var/lib/osckar/images
echo 'Done'

