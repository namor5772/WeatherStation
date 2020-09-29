#!/bin/bash

cd /
cd /sys/class/leds/led1

sudo sh -c "echo timer > trigger"
cat delay_on
cat delay_off

echo "led1 timer" 