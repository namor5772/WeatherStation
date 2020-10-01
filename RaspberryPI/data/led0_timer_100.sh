#!/bin/bash

cd /
cd /sys/class/leds/led0

sudo sh -c "echo timer > trigger"
sudo sh -c "echo 100 > delay_on"
sudo sh -c "echo 100 > delay_on"
cat delay_on
cat delay_off

echo "led0 timer" 