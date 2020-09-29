#!/bin/bash

cd /
cd /sys/class/leds/led1
sudo sh -c "echo 0 > brightness"

echo "led1 off" 