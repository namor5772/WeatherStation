#!/bin/bash

cd /
cd /sys/class/leds/led0

sudo sh -c "echo timer > trigger"
sudo sh -c "echo 2000 > delay_on"
sudo sh -c "echo 2000 > delay_off"
cat delay_on
cat delay_off

echo "led0 timer" 