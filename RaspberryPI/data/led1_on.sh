#!/bin/bash

cd /
cd /sys/class/leds/led1
sudo sh -c "echo 1 > brightness"

echo "led1 on" 