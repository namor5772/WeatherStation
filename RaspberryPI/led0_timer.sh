#!/bin/bash

cd /
cd /sys/class/leds/led0

sudo sh -c "echo timer > trigger"
cat delay_on
cat delay_off

echo "led0 timer" 