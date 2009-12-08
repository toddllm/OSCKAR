#!/bin/sh

#install script for web_kiosckar
#written by rossca

#install dependencies
sudo apt-get install apache2 python

#copy files
sudo cp -r ./etc/* /etc/
sudo cp -r ./var/* /var/

#restart webserver (but don't ACTUALLY restart, just tell
#  user to restart manually)
echo 'web_kiosckar has been installed, BUT...'
echo ' '
echo 'You now need to restart Apache in order for new'
echo 'settings to take effect.  Do this by running the'
echo 'following command NOW (or when you are ready):'
echo ' '
echo '  sudo /etc/init.d/apache2 restart'
echo ' '
