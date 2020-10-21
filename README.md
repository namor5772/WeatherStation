# Weather Station

## **Contents**

- [Summary](#Summary)
- [Setup Raspberry PI](#Setup-Raspberry-PI)
- [Setup Arduino](#Setup-Arduino)
- [Build circuit board](#Build-circuit-board)
  - [Install TinyCAD](#Install-TinyCAD)
  - [Install VeeCAD](#Install-VeeCAD)
- [Assemble weather station](#Assemble-weather-station)
- [Use weather station](#Use-weather-station)
- [Design characteristics](#Design-characteristics)
- [List of parts](#List-of-parts)
  - [Core components](#Core-components)
  - [Connectors](#Connectors)
  - [External components](#External-components)
- [Miscellaneous](#Miscellaneous)

## Summary

![alt text](images/ws1.png "Weather station enclosure")

This document describes the design, building and programming of an IOT enabled weather station. At regular intervals (eg. every 10 minutes) it measures a range of weather and other statistics, saving them as time stamped rows to an updated csv file. In particular:

1. Temperature (C)
1. Pressure (HPa)
1. Humidity (%)
1. Rainfall (mm/h)
1. Wind speed (km/h)
1. Wind direction (deg)
1. CPU temp (C) - of the Raspberry Pi
1. Current (A) - being drawn from the solar panel charged battery
1. Voltage (V) - at the inputs to the circuits voltage regulator
1. Power (W) - drawn by the weather station ( as A*V above)

This data can be remotely accessed via a php nginx web server interface from the Raspberry Pi, which also enables add-hoc contol and data requests. There is also a camera (attached to the Raspberry Pi) which can be controlled to take pictures on demand.

The hardware is based on a Raspberry Pi 3A+ and an Arduino Leonardo together with a Vero strip board that contains the Voltage Regulator and all other "glue" circuits. Everything is powered by a 12V 100Ah AGM Deep Cycle Battery which is charged by a 12V 150W Solar panel via a PWM Solar charge controller. The 12V input is regulated to 5.2V for the Raspberry Pi. This is is also used as required for charging the wifi modem, powering the Arduino (from the Raspberry Pi), powering sensors, servos and the digital relay.

The Raspberry Pi runs the web server and a python program that operates a bi-directional serial communications channel with the Arduino. The latter is ultimately attached to the various weather sensors. It also controls the digital relay used to time the charging of the wifi modem (on a 12hrs overnight ON and 12hr daytime OFF cycle) and the servo used to reset it (either by explicit command or each midnight). Control messages are typically sent from the Raspberry Pi via the serial channel to the Arduino (running a C++ program) which then returns sensor results or performs requested actions and returns confirmation messages.

The wifi modem and servo are attched by loomed 2 metre cables to the Vero board. The temperatue, pressure and humidity sensor is similarily attached with 1 metre cables. The two RJ11 terminated 3 metre cables from the rainfall, windspeed and wind direction sensors also attach to the Vero board. The Vero board circuit logic was designed in TinyCAD and its layout in VeeCAD.

## Setup Raspberry PI

We are using a Raspberry Pi 3 Model A+.

Details on how to set it up are given [**HERE**](RaspberryPI/README.md).

## Setup Arduino

We are using a Arduino Leonardo (Without Headers).

Details on how to set it up are given [**HERE**](Arduino/README.md).

## Build circuit board

### Install TinyCAD

[**DOWNLOAD**](https://www.tinycad.net/Home/Download) and install TinyCAD if you don't already have it.

In addition we need the following files. They can reside in any directories (on the PC where TinyCAD is installed) when copied from here or recreated.

| File | Description |
| --- | --- |
| [V_RomansOwn2020.TCLib](data/V_RomansOwn2020.TCLib) | TinyCAD library file with needed custom symbols |
| [WeatherStationMain1.dsn](data/WeatherStationMain1.dsn) | Actual TinyCAD file for this projects circuit board |
| [WeatherStationMain1.net](data/WeatherStationMain1.net) | PCB netlist created in Protel format from above file |

Now install the above custom symbol library **V_RomansOwn2020.TCLib** from the main menu of TinyCAD: **Library=>Libraries..=>Add=>V_RomansOwn2020.TCLib=>Open=>Ok**

![alt text](images/TinyCAD1.png "Install custom TinyCAD library")

Finally we assume that all the generic TinyCAD and VeeCAD symbols libraries are installed and now we can open and view **WeatherStationMain1.dsn** with TinyCAD:

![alt text](images/WeatherStationMain1.png "WeatherStationMain1.dsn in TinyCAD")

With the above *.dsn file loaded we can check and recreate (if we want to) the Protel netlist file **WeatherStationMain1.net** (mentioned above). To avoid warnings filter the checking options as follows:

![alt text](images/TinyCAD2.png "TinyCAD netlist design rule checks")

Use **Special=>Create PCB Net List...=>Export**

![alt text](images/TinyCAD3.png "TinyCAD netlist creation dialog")

### Install VeeCAD

[**DOWNLOAD**](https://veecad.com/downloads.html) and install VeeCAD if you don't already have it.

In addition we need the following files. They can reside in any directories (on the PC where VeeCAD is installed) when copied from here.

| File | Description |
| --- | --- |
| [V_Standard_RMG.per](data/V_Standard_RMG.per) | Custom VeeCAD shape library file |
| [WeatherStationMain1.per](data/WeatherStationMain1.per) | Vero Board circuit layout file |

Our ultimate goal is to have a valid circuit layout file to help us build the hardware. To view it we just need to open **WeatherStationMain1.per** in VeeCAD.

![alt text](images/WeatherStationMain2.png "Vero Board circuit layout file")

We can also modify or recreate it by pressing: **Netlist=>Import=>Import** with **WeatherStationMain1.per** open and dialog set to:

![alt text](images/VeeCAD1.png "VeeCAD Import Netlist dialog")

## Assemble weather station

The following is the best view of **WeatherStationMain1.per** in VeeCAD for building the Vero board circuit. It displays component designators and not values.
Print it out 100% scale with the setups displayed below and stick it onto the track-free side of of an appropriately sized piece of Vero Board.

![alt text](images/VeeCAD2.png "Vero Board Print Setup")

![alt text](images/WeatherStationMain3.png "Vero Board circuit layout file - alt view ")

It is useful to print out a list of items (ie. designators) as shown below: **Board=>Materials=>Components=>Print**

![alt text](images/VeeCAD3.png "Vero Board circuit List of parts")

The component designators/Items can be matched to the List of Parts below for soldering. Below are several images of the Vero circuit board during construction. Note that J12 is missing by mistake and was installed later.

![alt text](images/vb3.png "Vero Board build - image #1")

![alt text](images/vb2.png "Vero Board build - image #2")

![alt text](images/vb1.png "Vero Board build - image #3")

Finally use **WeatherStationMain1.dsn**  to wire everything up.
![alt text](images/ws2.png "Weather station circuit board")

The servo has to be glued with araldite to the top of the wifi-dongle near its on/off button.
![alt text](images/wd1.png "Wifi Dongle with Servo attached")

## Use weather station

Once the weather station is running, it just sits there collecting weather data every 10 minutes and appending it to a csv file. It can be accessed and controlled via a web interface which is displayed below after the **help** command is submitted.

![alt text](images/iot1.png "web site - after help command")

The most important command is **gd** which displays a link to the most recently updated weather data file **SensorData.csv**. This can be downloaded and conveniently formatted and displayed in an Excel workbook.

![alt text](images/iot2.png "web site - after gd command")

The other commands are for fun, maintenance or testing. Note for instance the **tp** command which takes and displays a photo with the Raspberry PI camera:

![alt text](images/iot3.png "web site - after tp command")

### *THE END...*

## Design characteristics

TBC

## List of parts
  
### Core components

| Qty | Product | Description | AUD Cost | Comment | Designator____ |
| --- | --- | --- | --- | --- | --- |
|1 | [CE05971](https://core-electronics.com.au/raspberry-pi-3-model-a-plus.html) | Raspberry Pi 3 Model A+ | $44.51 | Used for internet connection/control and storing collected data | connected to J2 and J8. Also camera attached |
|1 | [A000052](https://core-electronics.com.au/arduino-leonardo-without-headers.html) | Arduino Leonardo (Without Headers) | $39.00 | Used to interface all sensors | connected to J3, J5, J6 and J9 |
|1 | [XC4514](https://jaycar.com.au/p/XC4514) | Arduino Compatible DC Voltage Regulator | $7.95 | Converts 12V battery power to 5.2V for all weather station needs. Use 4 pins from 40 Pin Header Terminal Strip to attach its corners to Vero board | U1 |
|1 | [XC4486](https://jaycar.com.au/p/XC4486) | Arduino Compatible Logic Level Converter Module | $4.95 | enables bidirecional serial comms between Raspberry Pi and Arduino boards | B1 |
|1 | [ADA4226](https://core-electronics.com.au/adafruit-ina260-high-or-low-side-voltage-current-power-sensor.html) | Adafruit INA260 High or Low Side Voltage, Current, Power Sensor | $22.51 | measures power and voltage used by total circuit. Attach to Vero board using supplied 8 Pin Header Terminal Strip | B2 |
|1 | [ADA2652](https://core-electronics.com.au/adafruit-bme280-i2c-or-spi-temperature-humidity-pressure-sensor.html) | Adafruit BME280 I2C or SPI Temperature Humidity Pressure Sensor | $45.02 | off board sensor used in shielded I2C mode | connected to J7 |
|1 | [SEN-15901](https://core-electronics.com.au/weather-meter-kit.html) | Weather Meter Kit | $144.80 | passive reed switch based wind speed, direction and rain sensors | connected to J10 and J11 |
|1 | [BOB-14021](https://core-electronics.com.au/sparkfun-rj11-breakout.html) | SparkFun RJ11 Breakout ( currently only need 1 ) | $2.95 | contains below RJ11 Connector. Attach to Vero board using a 6 Pin Header Terminal Strip | J10 |
|2 | [PRT-00132](https://core-electronics.com.au/rj11-6-pin-connector.html) | RJ11 6-Pin Connector ( currently only need 1 )| $3.78 | attaches to above breakout board | |
|1 | [SY4058](https://jaycar.com.au/p/SY4058) | 6V DIL SPDT Mini Relay | $7.95 | used to control charging of Wifi Modem | U2 |
|1 | [YM2758](https://jaycar.com.au/p/YM2758) | Arduino Compatible 9G Micro Servo Motor | $11.95 | used to "manually" reset Wifi Modem, connect with three 2M lengths of hookup wire | connected to J4 |
|1 | [CE04421](https://core-electronics.com.au/raspberry-pi-camera-board-v2-8-megapixels-38552.html) | Raspberry Pi Camera Board v2 - 8 Megapixels | $38.95 | just for interest | connected to cable below |
|1 | [ADA1731](https://core-electronics.com.au/flex-cable-for-raspberry-pi-camera-610mm-24.html) | Flex Cable for Raspberry Pi Camera - 610mm / 24" | $6.66 | longer than standard cable for flexibility | connected to Raspberry Pi and camera
|1 | [SN74HC00N](https://au.element14.com/texas-instruments/sn74hc00n/quad-2-input-nand-74hc00-dip14/dp/3120419?st=74hc00) | Logic IC, NAND Gate, Quad, 2 Inputs, 14 Pins, DIP, 74HC00 | $0.61 | part of hardware debounce circuit for wind speed and rain sensors | connected to U5 |
|1 | [SN74HC14N](https://au.element14.com/texas-instruments/sn74hc14n/ic-hex-inverter-schmitt-74hc14/dp/9591125?st=74hc14) | Logic IC, Inverter, Hex, 1 Inputs, 14 Pins, DIP, 74HC14 | $1.03 | part of hardware debounce circuit for wind speed and rain sensors | connected to U4 |
|2 | [PI6501](https://jaycar.com.au/p/PI6501) | 14 Pin Production (Low Cost) IC Socket| $0.80 | part of hardware debounce circuit for wind speed and rain sensors | U4, U5 |
|1 | [RR0596](https://jaycar.com.au/p/RR0596) | 10k Ohm 0.5 Watt Metal Film Resistors - Pack of 8 ( only need 3 )| $0.85 | part of hardware debounce and input circuit for Weather Meter Kit sensors | R3, R5, R6 |
|1 | [RR0572](https://jaycar.com.au/p/RR0572) | 1k Ohm 0.5 Watt Metal Film Resistors - Pack of 8 ( only need 3 ) | $0.85 | used in hardware debounce and relay circuits | R1, R2, R4 |
|1 | [ZT2152](https://jaycar.com.au/p/ZT2152) | BC547 NPN Transistor | $0.30 | used in relay circuit | Q1 |
|1 | [ZR1004](https://jaycar.com.au/p/ZR1004) | 1N4004 1A 400V Diode - Pack of 4 ( only need 1 )| $0.98 | used in relay circuit | D1 |
|2 | [MCCB](https://au.element14.com/multicomp/mccb1v104m2acb/cap-0-1-f-35v-20/dp/9708480) | Tantalum Capacitor, 0.1 µF, 35 V, MCCB Series, ± 20%, Radial Leaded, 5.08 mm | $4.34 | used in hardware debounce circuit for wind speed and rain sensors | C1, C2 |

### Connectors

| Qty | Product | Description | AUD Cost | Comment | Designator____ |
| --- | --- | --- | --- | --- | --- |
|1 | [HP9544](https://jaycar.com.au/p/HP9544) | PC Boards Vero Type Strip - 95mm x 305mm| $12.95 | Contains all circuits apart from Raspberry Pi and Arduino |
|1 | [WW4030](https://jaycar.com.au/p/WW4030) | Tinned Copper Wire - 100 gram Roll | $19.95 | for wiring up above Vero board |
|5 | [HM3414](https://jaycar.com.au/p/HM3414) | 4 Pin 0.1 Straight Locking Header - 2.54 pitch - Single | $2.00 | On Vero board to connect to Raspberry Pi, Arduino and BMP280 sensor | J2, J3, J7, J9 |
|6 | [HM3412](https://jaycar.com.au/p/HM3412) | 2 Pin 0.1 Straight Locking Header - 2.54 pitch - Single | $2.40 | On Vero board and Arduino for interconnection | J5, J6, J8 |
|1 | [HM3413](https://jaycar.com.au/p/HM3413) | 3 Pin 0.1 Straight Locking Header - 2.54 pitch - Single | $0.40 | On Arduino for connection to Vero board circuit |
|3 | [HM3172](https://jaycar.com.au/p/HM3172) | 2 Way PCB Mount Screw Terminals 5mm Pitch | $4.05 | On Vero board for external connections to 12V power, Raspberry Pi and wind direction sensor | J1, J11, J12 |
|1 | [HM3173](https://jaycar.com.au/p/HM3173) | 3 Way PCB Mount Screw Terminal - 5mm Pitch | $1.75 | On Vero board for external connection to Wifi Modem switching servo | J4 |
|1 | [PS0916](https://jaycar.com.au/p/PS0916) | USB TYPE A PC MOUNT Socket | $2.95 | on Vero board for power to Wifi Modem | U3 |
|1 | [HP0924](https://jaycar.com.au/p/HP0924) | M3 x 12mm Tapped Nylon Spacers - Pk.25 ( only need 14 )| $9.95 | For mounting Vero board, Raspberry Pi, Arduino and camera|
|1 | [HP0430](https://jaycar.com.au/p/HP0430) | 3mm Flat Steel Washers - Pk.25 ( only need 12 )| $3.00 | as above |
|1 | [HP0440](https://jaycar.com.au/p/HP0440) | M3 x 5mm Black Equipment Screws - Pk.25 ( only need 14 )| $2.30 | as above |
|1 | [HP0403](https://jaycar.com.au/p/HP0403) | M3 x 10mm Steel Screws - Pk.25 ( only need 12 )| $3.00 | For mounting Vero board, Raspberry Pi and Arduino |
|1 | [HM3212](https://jaycar.com.au/p/HM3212) | 40 Pin Header Terminal Strip ( only need 4 pins ) | $1.10 | for mounting power circuit XC4514 |
|1 | [WC6026](https://jaycar.com.au/p/WC6026) | 150mm Socket to Socket Jumper Leads - 40 Piece ( only need 20 ) | $5.95 | for connecting Vero board circuits to Raspberry Pi and Arduino |
|1 | [WC6024](https://jaycar.com.au/p/WC6024) | 150mm Plug to Plug Jumper Leads - 40 Piece ( only need 3 ) | $5.95 | for connecting Vero board circuits to Servo and other external sensors |
|1 | [WC7723](https://jaycar.com.au/p/WC7723) | 0.5m USB A male to Micro-B Cable ( can be 0.25m ) | $5.95 | To power Arduino from Raspberry Pi USD port |
|1 | [WC7757](https://jaycar.com.au/p/WC7757) | USB A to USB Micro B Cable 150mm | $4.95 | To power Vero board circuit from Raspberry Pi (USB not needed) |

### External components

| Qty | Product | Description | AUD Cost | Comment |
| --- | --- | --- | --- | --- |
|1 | [PP1970](https://jaycar.com.au/p/PP1970) | Marine Grade 10A Locking Lighter Plug | $7.95 | Used to get 12V power from Battery Box |
|1 | [WH3057](https://jaycar.com.au/p/WH3057) | 7.5 Amp 2 Core Tinned DC Power Cable -  3 metre | $4.80 | Connects above to main vero circuit board |
|1 | [SB1682](https://jaycar.com.au/p/SB1682) | 12V 100Ah AGM Deep Cycle Battery | $299.0 | stores all power for this weather station  
|1 | [ZM9135](https://jaycar.com.au/p/ZM9135) | 12V 150W Folding Solar Panel with 5M lead (discontinued) | $169.00 | used to charge above battery - has controller |
|1 | [HB8502](https://jaycar.com.au/p/HB8502) | Battery Box with Voltmeter and USB Charge | $99.95 | keeps battery safe and conveniently accessible |
|1 | [WH3000](https://jaycar.com.au/p/WH3000) | Red Light Duty Hook-up Wire - 25m ( only 3 metres needed ) | $5.95 | used for attaching external sensors/servo |
|1 | [WH3001](https://jaycar.com.au/p/WH3001) | Black Light Duty Hook-up Wire - 25m ( only 3 metres needed ) | $5.95 | used for attaching external sensors/servo |
|1 | [WH3004](https://jaycar.com.au/p/WH3004) | Yellow Light Duty Hook-up Wire - 25m ( only 2 metres needed ) | $5.95 | used for attaching external sensors/servo |
|1 | [WB1506](https://jaycar.com.au/p/WB1506) |  FIG 8 - OFC Shielded Audio Cable - Sold per metre - 1 metre )| $4.95 | used for attaching external I2C sensor |
|1 | [HP1225](https://jaycar.com.au/p/HP1225) | 10mm Loom Tube - 10 metres ( only 4 metres needed ) | $18.95 | keeps wires to external sensors and wifi dongle secure |
|1 | [WifiModem](https://www.telstra.com.au/internet/mobile-broadband/telstra-4gx-wifi-pro) | Telstra 4GX Wi-Fi Pro | $120.0 | connects weather station to the internet |
|1 | [COU2AMB02](https://www.officeworks.com.au/shop/officeworks/p/comsol-male-type-a-usb-2-0-to-male-mini-usb-cable-2m-cou2amb02) | USB A to Mini-B 2M Cable | $14.88 | power to above wifi dongle from Vero board power circuit |

## Miscellaneous

# Editing this GitHub Repository

All in a Windows 10 environment:

* Install GitHub Desktop
*  Install Visual Studio Code
* Setup start command prommt
  * This assumes Visual Studio 2019 Communiy Edition has been installed
  * installed   

The fox jumped over the lazy dog
