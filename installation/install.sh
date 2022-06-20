#!/bin/bash

# turn on bluetooth
echo "[LOG]: enabling bluetooth low energy..."
sudo hciconfig hci0 up
sudo btmgmt le on

#move service file to system dir
echo "[LOG]: creating service file..."
sudo mv -f wandeling.service /lib/systemd/system/

#permissions
sudo chmod 644 /lib/systemd/system/wandeling.service

#reload deamon
echo "[LOG]: setting up daemon..."
sudo systemctl daemon-reload
sudo systemctl enable wandeling.service

#install pip packages
echo "[LOG]: installing pip packages..."
sudo pip3 install -r requirements.txt 

echo "DONE!!!"