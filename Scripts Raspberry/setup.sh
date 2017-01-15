#!/bin/bash

### Tester la connexion i2c entre raspberry et arduino
i2cdetect -y 1
#i2cdetect -y 0

# Script de lancement
sudo chmod +x /home/pi/startup.sh
echo crontab -l | { echo "@reboot /home/pi/startup.sh"; } | crontab -

### Setup de la lib smbus néccessaire pour le polling
sudo apt-get install i2c-tools
sudo apt-get install python-smbus

### Pour le modèle B+ ajouter ceci à /boot/config.txt
device_tree=bcm2708-rpi-b-plus.dtb
device_tree_param=i2c1=on
device_tree_param=spi=on

### Setup de la lib pour le son
# Si neccessaire !!
sudo apt-get install alsa-utils
sudo modprobe snd_bcm2835
# Force la sortie jack
sudo amixer cset numid=1

# En fin
sudo reboot

# Configuration de l'écran
# A ajouter à /boot/config.txt
max_usb_current=1
hdmi_group=2
hdmi_mode=1
hdmi_mode=87
hdmi_cvt 1024 600 60 6 0 0 0
overscan_top=0
overscan_bottom=0
overscan_left=1
overscan_right=1

