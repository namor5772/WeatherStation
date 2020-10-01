#!/bin/bash

cd /
cd /sys/class/leds/led0
sudo sh -c "echo heartbeat > trigger"

echo "led0 heartbeat" 