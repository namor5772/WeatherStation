#!/bin/sh

cd /
cd /sys/class/leds/led0
sudo sh -c "echo 0 > brightness"

echo "led0 off" 