# WeatherStation

This document describes the design and programming of an IOT enabled weather station. At regular intervals (eg. every 10 minutes) it measures a range of weather and other statistics, saving them as time stamped rows to an updated csv file. In particular:
1. Temperature (C)
2. Pressure (HPa)
3. Humidity (%)
4. Rainfall (mm/h)
5. Wind speed (km/h)
6. Wind direction (deg)
7. CPU temp (C) - of the Raspberry Pi
8. Current (A) - being drawn from the battery
9. INA260 Voltage (V) - at the inputs to circuit voltage regulators
10. Power (W)

This data can be remotely accessed via a php nginx web server interface, which also enables add hoc contol and data requests. There is also a camera which can be be controlled to take pictures on demand.
