#!/bin/sh

# 0 to 100
QUALITY=$1

# image width
WIDTH=$2

# image height
HEIGHT=$3

cd /
#cd home/pi/roman
cd var/www/html
#sudo raspistill -t 2000 -rot 180 -q $QUALITY -v -w $WIDTH -h $HEIGHT -o photo.jpg
sudo raspistill -t 2000 -q $QUALITY -v -w $WIDTH -h $HEIGHT -o photo.jpg

