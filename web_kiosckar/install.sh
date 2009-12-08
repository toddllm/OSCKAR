#!/bin/sh

#install script for web_kiosckar
#written by rossca

#install dependencies
sudo apt-get install apache2 python



#copy files
sudo cp -r ./etc/* /etc/
sudo cp -r ./var/* /var/
