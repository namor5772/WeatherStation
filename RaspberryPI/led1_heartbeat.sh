#!/bin/bash

cd /
cd /sys/class/leds/led1
sudo sh -c "echo heartbeat > trigger"

echo "led1 heartbeat" 