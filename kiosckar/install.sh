#!/bin/bash

user='kiosk'

#install dependencies, assuming OSCARcore is already installed
#TODO add check for existence of OSCARcore
#sudo apt-get install -y python

echo -n 'Installing kiosckar... '
sudo find . -name '*~' -exec rm {} \;
sudo cp -r ./usr/* /usr/
if [ ! -e /var/kiosckar/images ]
    then
    sudo mkdir -p /var/kiosckar/images
fi

if [ ! -e /etc/kiosckar/contracts ]
    then
    sudo mkdir -p /etc/kiosckar/contracts
fi
sudo groupadd kiosckar
sudo cp ./etc/kiosckar/kiosk_template.vmt /etc/kiosckar/
sudo chown -R :kiosckar /etc/kiosckar
sudo chmod -R g+w /etc/kiosckar/contracts
echo 'Done'

echo " "
echo "kioskckar can be run either by normal users, or additionally as a specialized kiosk-mode"
echo "user that guests to this system can use for launching personal virtual machines and appliances."
echo " "
#echo -n "Do you wish to create and configure a specialized kiosk-mode user? (Y/n) [default:Y]:"
#read create
if [ X$create == X ]
     then
     create='Y'
fi
if [ X$create != XY ]
     then
     exit 0
fi

#echo -n "Enter a name that users will login with to use kiosk [default:$user]:"
#read usern
if [ X$usern != X ]
    then
    user=$usern
fi

sudo grep "$user" /etc/passwd
if [ $? -eq 1 ]
    then
    echo "Creating $user user..."
    sudo useradd -G libvirtd,kiosckar -m -s /usr/local/bin/kiosckar $user
    sudo passwd $user
fi

#echo 'Adding contents to xinit files... '
#echo 'exec xterm /usr/local/bin/kiosckar' | sudo tee /home/$user/.xsession 2>&1 > /dev/null
#echo 'exec xterm /usr/local/bin/kiosckar' | sudo tee /home/$user/.xinitrc 2>&1 > /dev/null

echo -n "Setting default window manager for $user user to kiosckar-wm... "
echo '[Desktop]' | sudo tee /home/$user/.dmrc > /dev/null 2>&1 
echo 'Session=kiosckar' | sudo tee -a /home/$user/.dmrc > /dev/null 2>&1
echo 'Done'
