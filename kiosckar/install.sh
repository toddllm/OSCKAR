#!/bin/bash

user='kiosk'

#install dependencies, assuming OSCARcore is already installed
#TODO add check for existence of OSCARcore
#sudo apt-get install -y python

sudo grep "$user" /etc/passwd
if [ $? -eq 1 ]
    then
    echo "Creating $user user..."
    sudo useradd -m -s /usr/local/bin/kiosckar $user -G libvirtd
    sudo passwd $user
fi

echo 'Adding contents to xinit files... '
echo 'exec xterm /usr/local/bin/kiosckar' | sudo tee /home/$user/.xsession 2>&1 > /dev/null
echo 'exec xterm /usr/local/bin/kiosckar' | sudo tee /home/$user/.xinitrc 2>&1 > /dev/null

echo -n 'Installing kiosckar... '
sudo find . -name '*~' -exec rm {} \;
sudo cp -r ./usr/local/bin/* /usr/local/bin/
if [ ! -e /var/kiosckar/images ]
    then
    sudo mkdir -p /var/kiosckar/images
fi

if [ ! -e /etc/kiosckar/contracts ]
    then
    sudo mkdir -p /etc/kiosckar/contracts
fi
sudo cp ./etc/kiosckar/kiosk_template.vmt /etc/kiosckar/
sudo chown -R $user /etc/kiosckar
echo 'Done'