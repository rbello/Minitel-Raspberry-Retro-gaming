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

### Configuration de raspi-config
# Ajouter "i2c-dev" au fichier /etc/modules
# Activer le port I2C dans les options avancées

# Ajouter dans /boot/config.txt  (pour la Rpi 3, si ce dtparam n'existe pas)
# dtparam=i2c1=on
# dtparam=i2c_arm=on

### Setup de la lib pour le son
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