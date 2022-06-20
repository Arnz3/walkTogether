#!/bin/bash

# turn on bluetooth
sudo hciconfig hci0 up
sudo btmgmt le on

#move service file to system dir
sudo mv -f wandeling.service /lib/systemd/system/

#permissions
sudo chmod 644 /lib/systemd/system/wandeling.service

#reload deamon
sudo systemctl daemon-reload
sudo systemctl enable wandeling.service

#install pip packages
sudo pip3 install -r requirements.txt 