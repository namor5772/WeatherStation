#!/bin/bash

cd /
cd /sys/class/leds/led1

sudo sh -c "echo timer > trigger"
sudo sh -c "echo 2000 > delay_on"
sudo sh -c "echo 2000 > delay_off"
cat delay_on
cat delay_off

echo "led1 timer" 