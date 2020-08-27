# WeatherStation

## Summary
This document describes the design and programming of an IOT enabled weather station. At regular intervals (eg. every 10 minutes) it measures a range of weather and other statistics, saving them as time stamped rows to an updated csv file. In particular:
1. Temperature (C)
2. Pressure (HPa)
3. Humidity (%)
4. Rainfall (mm/h)
5. Wind speed (km/h)
6. Wind direction (deg)
7. CPU temp (C) - of the Raspberry Pi
8. Current (A) - being drawn from the solar panel charged battery
9. INA260 Voltage (V) - at the inputs to the circuits voltage regulators
10. Power (W)

This data can be remotely accessed via a php nginx web server interface from the Raspberry Pi, which also enables add hoc contol and data requests. There is also a camera (attached to the Raspberry Pi) which can be be controlled to take pictures on demand.

The hardware is based on a Raspberry Pi and an Arduino MEGA, powered by a 12V 100Ah AGM Deep Cycle Battery which is charged by a 12V 150W Solar panel via a PWM Solar charge controller. The 12V input is regulated to 5.2V for the Raspberry Pi and 9.0V for the Arduino. These voltages are also used as required for charging the wifi dongle, powering sensors, servos and digital relays. The Raspberry Pi runs the web server and a python program that operates a bi-directional serial communications channel with the Arduino. The latter is attached to the various weather sensors. It also controls the digital relay used to time the charging of the wifi dongle and the servo used to reset it. Control messages are typically sent from the Raspberry Pi via the serial channel to the Arduino (running a C++ program) which then returns sensor results or performs requested actions and returns confirmation messages.         

## LIST OF PARTS
| Qty | Product | Description |
| --- | ---- | --- |
|1 | [XC9001](https://jaycar.com.au/p/XC9001) | Raspberry Pi 3B+ Single Board Computer |
|1 | [XC4486](https://jaycar.com.au/p/XC4486) | Arduino Compatible Logic Level Converter Module |
|1 | [XC4414](https://jaycar.com.au/p/XC4414) | Duinotech Nano Board - Arduino Compatible |
| | | Some double sided and single sided tape |