#!/bin/bash

#turn on (-x) off (+x) debugging 
set -x

username=`whoami`
if [[ $username == "root" && "x${1}" == "x" ]]
then
    echo 'if running as root, pass your username as the first argument'
    echo "example $0 username"
    exit 1
fi

if [ $username == "root" ]
then
    username=$1
fi
echo $username

#detect supported platforms
release=`grep DISTRIB_RELEASE /etc/lsb-release  | awk -F\= '{ print $2}'` 
if [ X$release != X9.04 ]
then
    echo 'Ubuntu 9.04 is the only fully supported platform at this time'
    exit 1
fi

#install dependencies
sudo apt-get -y install ubuntu-virt-mgmt qemu expect nmap

#copy oapvm binaries to install_dir
sudo cp -r ./etc/* /etc/
sudo cp ./oapvm/oapvm* /usr/local/bin/

#patch vmbuilder due to bugs
sudo patch -p0 -N < ./patches/vmbuilder.patch
sudo patch -p0 -N < ./patches/jdstrand.patch
sudo patch -p0 -N < ./patches/jdstrand2.patch
#create base VM

datetimestamp=`date +%F-%H_%M_%S`
sudo vmbuilder kvm ubuntu --libvirt=qemu:///system \
    --hostname ubuntu-amd64-desktop-base --addpkg ubuntu-desktop \
    --addpkg openssh-server --removepkg apt-xapian-index --user osckar \
    --pass=osckar --ssh-user-key=/etc/osckar/oapvm/id_rsa.pub --debug -v \
    --rootsize=8000 --mem=512 --dest=/tmp/osckar--base-${datetimestamp}/

#put image in place
sudo mv /tmp/osckar--base-${datetimestamp}/disk0.qcow2 \
    /etc/osckar/oapvm/vms/thin-ubuntu-base.qcow2


#disable current libvirt networks, install osckar network files
sudo mkdir /etc/libvirt/qemu/networks/disabled/
sudo mv /etc/libvirt/qemu/networks/*.xml /etc/libvirt/qemu/networks/disabled/
sudo cp ./libvirt/qemu/networks/*.xml /etc/libvirt/qemu/networks/

#autostart the control bridge
sudo ln -s /etc/libvirt/qemu/networks/osckarcontrol.xml \
    /etc/libvirt/qemu/networks/autostart/

#autostart the nat bridge
sudo ln -s /etc/libvirt/qemu/networks/osckarnat.xml \
    /etc/libvirt/qemu/networks/autostart/

#restart libvirt for changes to take effect
sudo /etc/init.d/libvirt-bin restart

#add user to libvirtd group (requires logout/login)
sudo usermod  -a -G libvirtd $username
echo 'added user to libvirtd group, logout then log back in (or restart)'
echo 0