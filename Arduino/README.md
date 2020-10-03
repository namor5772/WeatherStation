# **Arduino setup**

## **Contents**

- [Hardware](#Hardware)
- [Code files](#Code-files)
- [Configuration](#Configuration)

## **Hardware**

For efficiency and convenience we use an Arduino Leonardo without headers.
The goal is to have it running the appropriate code and have it interface to sensors, a servo, a digital relay and the Raspberry PI. All these connections are made to the Vero board to which everything is linked.

In production it is powered by the Raspberry PI with a USB A male to Micro-B Cable. For programming this can be connected to a PC. The other connections are via various pads (detailed below) to which appropriate straight locking headers are soldered.

* 2 Pin 0.1 Straight Locking Header
  * 5V - supplies power to the Vero board
  * GND - connects to common ground on Vero board
* 2 Pin 0.1 Straight Locking Header
  * A1 - Not connected
  * A2 - Wind Vane
* 2 Pin 0.1 Straight Locking Header
  * SCL - for I2C sensors
  * SCA - for I2C sensors
* 2 Pin 0.1 Straight Locking Header
  * D9 - Anemometer interrupt flag
  * D8 - Rain guage interrupt flag
* 3 Pin 0.1 Straight Locking Header
  * D7 - Common interrupt (only one available)
  * D6 - PWM for conrolling servo
  * D5 - For controlling Relay
* 2 Pin 0.1 Straight Locking Header
  * TX-> - serial comms with Raspberry PI
  * RX<- - serial comms with Raspberry PI

![alt text](images/Leonardo1.png "Leonardo1")

![alt text](images/Leonardo2.png "Leonardo2")


that is needed on this Raspberry PI. Once completed we will have an SD card that boots to the intended IOT environment.

## **Code files**

Go to <https://www.raspberrypi.org/downloads> and download the Raspberry PI imager (for Windows).

## **Configuration**

Arduino Leonardo

