# WeatherStation

[README2.md](README2.md)

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
9. Voltage (V) - at the inputs to the circuits voltage regulator
10. Power (W) - drawn by the weather station ( as A*V above)

This data can be remotely accessed via a php nginx web server interface from the Raspberry Pi, which also enables add hoc contol and data requests. There is also a camera (attached to the Raspberry Pi) which can be be controlled to take pictures on demand.

The hardware is based on a Raspberry Pi 3A+ and an Arduino Leonardo together with a Vero strip board based that contains the Voltage Regulator and all other circuits. Everything is powered by a 12V 100Ah AGM Deep Cycle Battery which is charged by a 12V 150W Solar panel via a PWM Solar charge controller. The 12V input is regulated to 5.2V for the Raspberry Pi. This is is also used as required for charging the wifi dongle, powering the Arduino (from the Raspberry Pi), powering sensors, servos and the digital relay. The Raspberry Pi runs the web server and a python program that operates a bi-directional serial communications channel with the Arduino. The latter is ultimately attached to the various weather sensors. It also controls the digital relay used to time the charging of the wifi dongle and the servo used to reset it. Control messages are typically sent from the Raspberry Pi via the serial channel to the Arduino (running a C++ program) which then returns sensor results or performs requested actions and returns confirmation messages.
The wifi dongle and servo are attched by loomed 2 metre cables to the Vero board. The temperatue, pressure and humidity sensor is similarily attached with 1 metre cables. The two RJ11 terminated 3 metre cables from the rainfall, windspeed and wind direction sensors also attach to the Vero board.
The Vero board circuit logic was designed in TinyCAD and layout in VeeCAD

## List of parts

| Qty | Product | Description | AUD Cost |
| --- | ---- | --- | --- |
|1 | [CE05971](https://core-electronics.com.au/raspberry-pi-3-model-a-plus.html) | Raspberry Pi 3 Model A+ | $44.51 |
|1 | [A000052](https://core-electronics.com.au/arduino-leonardo-without-headers.html) | Arduino Leonardo (Without Headers)  | $39.00 |
|1 | [XC4514](https://jaycar.com.au/p/XC4514) | Arduino Compatible DC Voltage Regulator | $7.95 |
|1 | [XC4486](https://jaycar.com.au/p/XC4486) | Arduino Compatible Logic Level Converter Module | $4.95 |
|1 | [ADA4226](https://core-electronics.com.au/adafruit-ina260-high-or-low-side-voltage-current-power-sensor.html) | Adafruit INA260 High or Low Side Voltage, Current, Power Sensor | $22.51 |
|1 | [ADA2652](https://core-electronics.com.au/adafruit-bme280-i2c-or-spi-temperature-humidity-pressure-sensor.html) | Adafruit BME280 I2C or SPI Temperature Humidity Pressure Sensor | $45.02 |
|1 | [SEN-15901](https://core-electronics.com.au/weather-meter-kit.html) | Weather Meter Kit | $144.80 |
|1 | [BOB-14021](https://core-electronics.com.au/sparkfun-rj11-breakout.html) | SparkFun RJ11 Breakout ( currently only need 1 ) | $2.95 |
|2 | [PRT-00132](https://core-electronics.com.au/rj11-6-pin-connector.html) | RJ11 6-Pin Connector ( currently only need 1 )| $3.78 |
|1 | [SY4058](https://jaycar.com.au/p/SY4058) | 6V DIL SPDT Mini Relay | $7.95 |
|1 | [YM2758](https://jaycar.com.au/p/YM2758) | Arduino Compatible 9G Micro Servo Motor | $11.95 |
|1 | [CE04421](https://core-electronics.com.au/raspberry-pi-camera-board-v2-8-megapixels-38552.html) | Raspberry Pi Camera Board v2 - 8 Megapixels | $38.95 |
|1 | [ADA1731](https://core-electronics.com.au/flex-cable-for-raspberry-pi-camera-610mm-24.html) | Flex Cable for Raspberry Pi Camera - 610mm / 24" | $6.66 |
|1 | [SN74HC00N](https://au.element14.com/texas-instruments/sn74hc00n/quad-2-input-nand-74hc00-dip14/dp/3120419?st=74hc00) | Logic IC, NAND Gate, Quad, 2 Inputs, 14 Pins, DIP, 74HC00 | $0.61 |
|1 | [SN74HC14N](https://au.element14.com/texas-instruments/sn74hc14n/ic-hex-inverter-schmitt-74hc14/dp/9591125?st=74hc14) | Logic IC, Inverter, Hex, 1 Inputs, 14 Pins, DIP, 74HC14 | $1.03 |
|2 | [PI6501](https://jaycar.com.au/p/PI6501) | 14 Pin Production (Low Cost) IC Socket| $0.80 |
|1 | [RR0596](https://jaycar.com.au/p/RR0596) | 10k Ohm 0.5 Watt Metal Film Resistors - Pack of 8 ( only need 3 )| $0.85 |
|1 | [RR0572](https://jaycar.com.au/p/RR0572) | 1k Ohm 0.5 Watt Metal Film Resistors - Pack of 8 ( only need 3 ) | $0.85 |
|1 | [ZT2152](https://jaycar.com.au/p/ZT2152) | BC547 NPN Transistor | $0.30 |
|1 | [ZR1004](https://jaycar.com.au/p/ZR1004) | 1N4004 1A 400V Diode - Pack of 4 ( only need 1 )| $0.98 |
|2 | [MCCB1V104M2ACB](https://au.element14.com/multicomp/mccb1v104m2acb/cap-0-1-f-35v-20/dp/9708480) | Tantalum Capacitor, 0.1 µF, 35 V, MCCB Series, ± 20%, Radial Leaded, 5.08 mm | $4.34 |
|1 | [HP9544](https://jaycar.com.au/p/HP9544) | PC Boards Vero Type Strip - 95mm x 305mm| $12.95 |
|1 | [WW4030](https://jaycar.com.au/p/WW4030) | Tinned Copper Wire - 100 gram Roll | $19.95 |
|4 | [HM3414](https://jaycar.com.au/p/HM3414) | 4 Pin 0.1 Straight Locking Header - 2.54 pitch - Single | $2.00 |
|8 | [HM3412](https://jaycar.com.au/p/HM3412) | 2 Pin 0.1 Straight Locking Header - 2.54 pitch - Single | $2.40 |
|1 | [HM3413](https://jaycar.com.au/p/HM3413) | 3 Pin 0.1 Straight Locking Header - 2.54 pitch - Single | $0.40 |
|3 | [HM3172](https://jaycar.com.au/p/HM3172) | 2 Way PCB Mount Screw Terminals 5mm Pitch | $4.05 |
|1 | [HM3173](https://jaycar.com.au/p/HM3173) | 3 Way PCB Mount Screw Terminal - 5mm Pitch | $1.75 |
|1 | [PS0916](https://jaycar.com.au/p/PS0916) | USB TYPE A PC MOUNT Socket | $2.95 |
|1 | [HP0924](https://jaycar.com.au/p/HP0924) | M3 x 12mm Tapped Nylon Spacers - Pk.25 ( only need 14 )| $9.95 |
|1 | [HP0430](https://jaycar.com.au/p/HP0430) | 3mm Flat Steel Washers - Pk.25 ( only need 12 )| $3.00 |
|1 | [HP0440](https://jaycar.com.au/p/HP0440) | M3 x 5mm Black Equipment Screws - Pk.25 ( only need 14 )| $2.30 |
|1 | [HP0403](https://jaycar.com.au/p/HP0403) | M3 x 10mm Steel Screws - Pk.25 ( only need 12 )| $3.00 |
|1 | [HM3212](https://jaycar.com.au/p/HM3212) | 40 Pin Header Terminal Strip ( only need 4 pins ) | $1.10 |
|1 | [WC6026](https://jaycar.com.au/p/WC6026) | 150mm Socket to Socket Jumper Leads - 40 Piece ( only need 20 ) | $5.95 |
|1 | [WC6024](https://jaycar.com.au/p/WC6024) | 150mm Plug to Plug Jumper Leads - 40 Piece ( only need 3 ) | $5.95 |
|1 | [WH3057](https://jaycar.com.au/p/WH3057) | 7.5 Amp 2 Core Tinned DC Power Cable -  3 metre | $4.80 |
|1 | [PP1970](https://jaycar.com.au/p/PP1970) | Marine Grade 10A Locking Lighter Plug | $7.95 |
|1 | [SB1682](https://jaycar.com.au/p/SB1682) | 12V 100Ah AGM Deep Cycle Battery | $299.0 |
|1 | [ZM9135](https://jaycar.com.au/p/ZM9135) | 12V 150W Folding Solar Panel with 5M lead (discontinued) | $169.00 |
|1 | [HB8502](https://jaycar.com.au/p/HB8502) | Battery Box with Voltmeter and USB Charge | $99.95 |
|1 | [WH3000](https://jaycar.com.au/p/WH3000) | Red Light Duty Hook-up Wire - 25m ( only 3 metres needed ) | $5.95 |
|1 | [WH3001](https://jaycar.com.au/p/WH3001) | Black Light Duty Hook-up Wire - 25m ( only 3 metres needed ) | $5.95 |
|1 | [WH3004](https://jaycar.com.au/p/WH3004) | Yellow Light Duty Hook-up Wire - 25m ( only 3 metres needed ) | $5.95 |
|1 | [WH3007](https://jaycar.com.au/p/WH3007) | White Light Duty Hook-up Wire - 25m ( only 2 metres needed )| $5.95 |
|1 | [WC7723](https://jaycar.com.au/p/WC7723) | 0.5m USB A male to Micro-B Cable ( can be 0.25m ) | $5.95 |
|1 | [WC7757](https://jaycar.com.au/p/WC7757) | USB A to USB Micro B Cable 150mm | $4.95 |
|1 | [HP1225](https://jaycar.com.au/p/HP1225) | 10mm Loom Tube - 10 metres ( only 4 metres needed) | $18.95 |
