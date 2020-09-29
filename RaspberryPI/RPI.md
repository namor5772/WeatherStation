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

Their only purpose is to setup bidirectional serial communications to the Arduino.

## Software
Go to https://www.raspberrypi.org/downloads/ and download the Raspberry PI imager (for Windows).

With a 32GB micro SD Card and adaptor attached to your Windows 10 PC select the RASPBERRY PI OS (32BIT) option and then the above SD card. Finally press WRITE and wait.

	• You can now put the SD card into your Raspberry PI. Have a dongle for bluetooth keyboard and mouse. Also HDMI monitor plugged in
		○ Follow prompts on first boot.
		○ Change password to: xxxxxxxx
		○ Select WiFi Network: xxxxxxxx, Password: xxxxxxxx
		○ Make sure wifi working to enable software update - takes ages!
		○ Restart when requested.
	• In terminal window type
		○ sudo apt update
		○ sudo apt install python3 idle3
		○ as at 4/05/2020 this installs Python 3.7.3 with IDLE 3.7.3 and Tk 8.6.9.
			○ This information is available in the GUI from the Application Menu => Programming => Python 3 (IDLE)
	• Install nginx, mysql and php for Python 3 on the Raspberry PI:
		○ As per the below link.
		○ Note: mariadb seems to replace mysql
	• Set Raspberry Pi Configuration, only changing:
		○ System => Hostname: rp3b
		○ Interfaces Enable: Camera, SSH, I2C, Serial Port, Remote GPIO
	• Setup Dataplicity:
		○ As per below link.
		○ Add this Raspberry PI as a new device, possibly deleting the one from the old Raspberry PI.
		○ Follow the other steps if necessary.
	• Download backup files needed for IOT. Python, cpp, scripts etc.
		○ Use a dongle if cannot get WinSCP to work
		○ You will need to create the home/pi/roman 
		○ Run "sudo chmod -R 777 /var/www/html" to be able to add files to that directory.
			○ The index.php file should have permissions -rwxrwxrwx root root
		○ copy files detailed in the sections
			○ The main rebooting script is:
			○ The "container" Python script is:
			○ The actual Python script is:
			○ Client side:
