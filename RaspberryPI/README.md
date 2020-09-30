# Raspberry PI

The goal is to launch a python script on reboot of the Raspberry PI and have the script restart if it crashes.
We are using a Raspberry PI 3A+ and run all scripts using Python 3 which we assume has been installed.

[Install](#Install_nginx)

## Hardware

Raspberry PI 3A+. We are using this version since it uses less power, is cheaper, has a smaller form factor but has wifi and the one USB port is sufficient.

It is powered by 5.2V and when in production the one USB connection is used to power the Arduino Leonardo board. Apart from the above the only connections are via 4 GPIO pins.
* GPIO 1 - 3.3V
* GPIO 6 - GROUND
* GPIO 8 - UART TXD
* GPIO 10 - UART RXD

Their only purpose is to setup bidirectional serial communications to the Arduino.

## SD Card

Go to https://www.raspberrypi.org/downloads/ and download the Raspberry PI imager (for Windows).

With a 32GB micro SD Card and adaptor attached to your Windows 10 PC select the RASPBERRY PI OS (32BIT) option and then the above SD card. Finally press WRITE and wait.

![alt text](images/Imager.png "Raspberry Pi Imager")

* You can now put the SD card into your Raspberry PI. Have a dongle for bluetooth keyboard and mouse. Also a HDMI monitor plugged in:
  - Follow prompts on first boot.
  - Change password to: RPIPWD
  - Select WiFi Network: WIFISSID, Password: WIFIPWD
	- Make sure wifi working to enable software update - takes ages!
	- Restart when requested.
* In a terminal window type
	- sudo apt update
	- sudo apt install python3 idle3
	-	as at 30/09/2020 this installs Python 3.7.3 with IDLE 3.7.3 and Tk 8.6.9.
		- This information is available in the GUI from the Application Menu => Programming => Python 3 (IDLE) => Help => About IDLE
* Set Raspberry Pi Configuration, only changing:
	- System => Hostname: HOSTNAME
	- Interfaces Enable: **Camera, SSH, I2C, Serial Port, Remote GPIO**




	• Install nginxl and php
		○ As per the below link.
		○ Note: mariadb seems to replace mysql
		
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

[Soft](#Software)

## Install nginx & php

* In a terminal window type
	- cd /
	- pip3 --version (just for information)
	- sudo apt-get update
	- sudo apt-get install nginx
	- sudo /etc/init.d/nginx start
	- sudo netstat -an | grep LISTEN | grep :80
		- This checks that a service is listening on port 80. It should show something like:				
![alt text](images/nginx.png "nginx service listening")

	- sudo service nginx restart (It doesn't hurt)
	- sudo apt install php-fpm
	- cd /etc/nginx
	- sudo nano sites-enabled/default
		- Find the line "index index.html index.htm;"
		- Add "index.php" after "index" in above line
		- Find the line "# location ~ \.php$ {"
		- and add the following lines or remove # till the next "}"


				include snippets/fastcgi-php.conf;
				fastcgi_pass unix:/var/run/php/php7.3-fpm.sock;


		-	It should look like

				location ~ .php$ {
					include snippets/fastcgi-php.conf;
					fastcgi_pass unix:/var/run/php/php7.3-fpm.sock;
					}

		- Save the above edited file and reload
			- sudo /etc/init.d/nginx reload 

* To test the server:
	- find the address on the Raspberry PI
		- hostname -I
		- it will give you something like 192.168.0.12
		- type http://192.168.0.12 in the browser of another PC attached to the local network:
![alt text](images/nginxtest.png "nginx test")


		
		
	• To make nginx restart if it crashes non gracefully (it has happened):
		○ Go to /lib/systemd/system and backup the nginx systemd unit (just in case)
			§ cd /
			§ cd /lib/systemd/system
			§ sudo cp nginx.service nginx.service.old
		○  Add the following 2 lines at the end of the [Service] block of nginx.service
				□ Restart=on-failure
				□ RestartSec=9s
			§ Do this by typing: sudo nano nginx.service
			§ Saving the edited nginx.service file: Ctrl-X, Y, Enter.
		○ load the new config:
			§ sudo systemctl daemon-reload
		○ To test kill nginx:
			§ cd /
			§ cd var/run
			§ cat nginx.pid (will give you the PID)
			§ sudo kill -9 PID
			§ The nginx process will restart with a different PID (as can be viewed through the Task Manager)

	• To test PHP  
		○ cd /
		○ cd var/www/html
		○ sudo chmod o+w /var/www/html (to enable copying into this folder for later)
		○ sudo nano index.nginx-debian.html (being the default web page)
		○ Add the below lines just above the </body> tag:
			§ <?php
			§ phpinfo();
			§ ?>
		○ Save the file as index.php
		○ View http://192.168.0.12 again

		
			location ~ .php$ {
				include snippets/fastcgi-php.conf;
				fastcgi_pass unix:/var/run/php/php7.0-fpm.sock;
				}
		

