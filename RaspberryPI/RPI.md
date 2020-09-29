# Raspberry PI

The goal is to launch a python script on reboot of the Raspberry PI and have the script restart if it crashes.
We are using a Raspberry PI 3A+ and run all scripts using Python 3 which we assume has been installed.

## Hardware

Raspberry PI 3A+. We are using this version since it uses less power, is cheaper, has a smaller form factor but has wifi and the one USB port is sufficient.

It is powered by 5.2V and when in production the one USB connection is used to power the Arduino Leonardo board. Apart from the above the only connections are via 4 GPIO pins.
* GPIO 1 - 3.3V
* GPIO 6 - GROUND
* GPIO 8 - UART TXD
* GPIO 10 - UART RXD 

Their only purpose is to setup bidirectional serial communications to the Arduino

## Software

