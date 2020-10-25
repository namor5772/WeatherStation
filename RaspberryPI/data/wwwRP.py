#!/usr/bin/python3
import serial
import io
import time
import datetime
import codecs
import subprocess
import csv
import filecmp
import shutil


k=0
#setup serial connection to Arduino
ser = serial.Serial('/dev/ttyS0',4800,timeout=2.0)
bSerial = False


# Runs a shell script *.sh assumed to reside in home/pi/roman and having been
# made executable. First line is assumed to be #!/bin/bash
# no arguments
def RunShellScript(ScriptFile):
    cmd=['sh', '/home/pi/roman/'+ScriptFile+'.sh']
    proc = subprocess.Popen(cmd,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    o,e = proc.communicate()
    outstr = o.decode('ascii')
    errstr = e.decode('ascii')
    retstr = str(proc.returncode)
    print ('Output: '+outstr)
    print ('Error: '+errstr)
    print ('code: '+retstr)
    return outstr


# Runs a shell script *.sh assumed to reside in home/pi/roman and having been
# made executable. First line is assumed to be #!/bin/bash
# 3 arguments
def RunShellScript_arg(ScriptFile,arg1,arg2,arg3):
    print(arg1,arg2,arg3)
    cmd=['sh', '/home/pi/roman/'+ScriptFile+'.sh',str(arg1),str(arg2),str(arg3)]
    proc = subprocess.Popen(cmd,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    o,e = proc.communicate()
    outstr = o.decode('ascii')
    errstr = e.decode('ascii')
    retstr = str(proc.returncode)
    print ('Output: '+outstr)
    print ('Error: '+errstr)
    print ('code: '+retstr)
    return outstr


# Runs a shell script *.sh assumed to reside in home/pi/roman and having been
# made executable. First line is assumed to be #!/bin/bash
# 7 arguments
def RunShellScript_arg7(ScriptFile,arg1,arg2,arg3,arg4,arg5,arg6,arg7):
    print(arg1,arg2,arg3,arg4,arg5,arg6,arg7)
    cmd=['sh', '/home/pi/roman/'+ScriptFile+'.sh',str(arg1),str(arg2),str(arg3),str(arg4),str(arg5),str(arg6),str(arg7)]
    proc = subprocess.Popen(cmd,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    o,e = proc.communicate()
    outstr = o.decode('ascii')
    errstr = e.decode('ascii')
    retstr = str(proc.returncode)
    print ('Output: '+outstr)
    print ('Error: '+errstr)
    print ('code: '+retstr)
    return outstr


# Returns start time - EXPAND LATER
def CollectDataStartTime(minGap):
    # assume min gap dvides 60 minutes in hour ie is (1,2,4,5,6,10,12,15,20,30,60)
    dtn = datetime.datetime.now()
    dtny = dtn.year
    dtnm = dtn.month
    dtnd = dtn.day
    dtnh = dtn.hour
    dtnmi = dtn.minute

    # largest integer number of minGap's that are less than dtnmi
    sm = (dtnmi//minGap)*minGap
    print(sm)

    ist = datetime.datetime(dtny,dtnm,dtnd,dtnh,sm)
    dtd = datetime.timedelta(days=0,hours=0,minutes=minGap)
    ist = ist+dtd

    print(ist.strftime('%d-%b-%Y %H:%M:%S'))
    return ist


# Returns start time 2 - EXPAND LATER
def CollectDataStartTime2(hourGap):
    dtn = datetime.datetime.now()
    dtny = dtn.year
    dtnm = dtn.month
    dtnd = dtn.day
    dtnh = dtn.hour
    dtnmi = dtn.minute

    # largest integer number of hourGap's that are less than dtnh
    sm = (dtnh//hourGap)*hourGap
    print(sm)

    ist = datetime.datetime(dtny,dtnm,dtnd,sm,0)
    dtd = datetime.timedelta(days=0,hours=hourGap,minutes=0)
    ist = ist+dtd

    print(ist.strftime('%d-%b-%Y %H:%M:%S'))
    return ist


n=0
n2=0

# gap in minutes between data collection events (assume 60 % minGap == 0)
minGap = 15
hourGap = 24

# data collection time gap
dtd = datetime.timedelta(days=0,hours=0,minutes=minGap,seconds=0)

# action repeat time gap 2
dtd2 = datetime.timedelta(days=0,hours=hourGap,minutes=0,seconds=0)

# initial future time at which we will start collecting data
actTime = CollectDataStartTime(minGap)

# initial future time at which we will start repeating action
actTime2 = CollectDataStartTime2(hourGap)

# when first started do this to avoid spurious client command
shutil.copyfile('/var/tmp/text.txt','/var/tmp/text_bak.txt')

# wifi power flag (0=off, 1=on) and related variables
wifipower = 1 # default is wifi power ON
OFF_hr, OFF_min = 8, 1 # hour & min of day when wifi power is turned off
ON_hr, ON_min = 20, 1 # hour & min of day when wifi power is turned back on
powerOFFtime = datetime.time(OFF_hr,OFF_min,0,0)
powerONtime = datetime.time(ON_hr,ON_min,0,0)

# variables related to turining the wifi dongle off and then back on automatically after a set time.
wifiTimeOFF = 5 # default time in minutes for which wifi will be turned off.
dtd3 = datetime.timedelta(days=0,hours=0,minutes=wifiTimeOFF,seconds=10)
wifiTURN_ON = False # default state is that we do not want to turn the wifi on
WIFIactTime = actTime # just for initialisation


try:
    while True:
        dtn = datetime.datetime.now()
        dtns = dtn.strftime('%d%b%Y-%H:%M:%S')
        tx = dtn.strftime('%H%M%S')+"\r\n"
        dtnt = dtn.time() # the time of now (ignores date)

        # action wifi charging management
        if ((wifipower==1) and (dtnt > powerOFFtime) and (dtnt <= powerONtime)):
            # turn wifi power OFF
            while bSerial:
                time.sleep(1.0)
            bSerial = True
            ser.write(b'y')
            bSerial = False
            wifipower=0
        elif ((wifipower==0) and (dtnt > powerONtime)):
            # turn wifi power ON
            while bSerial:
                time.sleep(1.0)
            bSerial = True
            ser.write(b'x')
            bSerial = False
            wifipower=1

        # turn wifi on as required at WIFIactTime (which is wifiTimeOFF minutes + 10 seconds after it was turned off)
        if ((dtn >= WIFIactTime) and wifiTURN_ON):
            while bSerial:
                time.sleep(1.0)
            bSerial = True
            ser.write(b's')
            msg = "Pressed the wifi dongle button for 6 seconds"
            print(msg)
            bSerial = False
            wifiTURN_ON = False

        # do data collection stuff in main loop every minGap minutes
        if dtn >= actTime:
            n=n+1
            ats = actTime.strftime('%d-%b-%Y %H:%M:%S')
            print(" ")
            print("MAIN LOOP =",n)
            print("at time =",ats)
            actTime = actTime + dtd

            # collect CPU temperature in C to 1dp
            shellscript = 'cputemp'
            outstr = RunShellScript(shellscript)
            tCPU = str('{:.1f}'.format(round(float(outstr.strip())/1000.0,1)))
            print(tCPU)
            print(" ")

            # collect temperature, pressure, humidity, rainfall, wind speed, wind direction,
            # current, Bus Voltage and power by sending serial message (char u) to Arduino Mega
            while bSerial:
                time.sleep(1.0)
            bSerial = True
            ser.write(b'u')
            time.sleep(4.0) # to give time for serial reply from Arduino
            te, pr, hu, rf, ws, wd, cu, bv, po = str(ser.read_until(b'\r\n'))[2:-5].split( )
            te = str('{:.1f}'.format(round(float(te),1))) # temperature in C 1dp
            pr = str('{:.1f}'.format(round(float(pr),1))) # pressure in hPa 1dp
            hu = str('{:.1f}'.format(round(float(hu),1))) # humidity in % 1dp
            rf = str('{:.1f}'.format(round(float(rf),1))) # rain in mm idp
            ws = str('{:.1f}'.format(round(float(ws),1))) # wind speed in km/hr 1dp
            wd = str('{:.1f}'.format(round(float(wd),1))) # wind direction in degrees 1dp
            cu = str('{:.3f}'.format(round(float(cu)/1000.0,3))) # current in A 3dp
            bv = str('{:.2f}'.format(round(float(bv)/1000.0,2))) # Bus Voltage in V 2dp
            po = str('{:.2f}'.format(round(float(po)/1000.0,2))) # power in W 2dp
            bSerial = False
            print(te,pr,hu,rf,ws,wd,cu,bv,po," ")

            # Append collected data to data file with a time stamp
            odf = open('/var/www/html/SensorData.csv','a',newline='')
            odw = csv.writer(odf)
            odw.writerow([ats,te,pr,hu,rf,ws,wd,tCPU,cu,bv,po])
            odf.close()
                
        # perform actions in main loop 2
        if dtn >= actTime2:
            n2=n2+1
            ats = actTime2.strftime('%d-%b-%Y %H:%M:%S')
            print(" ")
            print("MAIN LOOP2 =",n2)
            print("at time =",ats)
            actTime2 = actTime2 + dtd2

            # press the wifi dongle button for 6 seconds.
            while bSerial:
                time.sleep(1.0)
            bSerial = True
            ser.write(b's')
            bSerial = False
            msg = "Pressed the wifi dongle button for 6 seconds"
            print(msg," ")

        # see if text.txt file has changed compared to text_bak.txt
        bSame = filecmp.cmp('/var/tmp/text.txt','/var/tmp/text_bak.txt')
        if not bSame:
            print('Received Command from client')

            # parse contents of text.txt file
            f = open('/var/tmp/text.txt',"r")
            msgs = str(f.read())
            sBody = msgs[6:]
            sBodyArg = sBody.split()
            print(dtns)
            print(sBody)
            print(sBodyArg)
            print(len(sBodyArg))
            f.close()

            # make text_bak same as text in preperation for next command
            shutil.copyfile('/var/tmp/text.txt','/var/tmp/text_bak.txt')

            # act on command from text.txt file
            try:
                if (sBodyArg[0] == 'help'):
                    # meaning: show help
                    f = open('/var/tmp/result.txt','w')
                    f.writelines([tx,"\r\n",
                                     "Note: All inputs are NOT case sensitive\r\n",
                                     "help - display this help\r\n",
                                     "gd - enable link to current sensor data file\r\n",
                                     "LDG - display photo of Lidia Duda-Groblicka in her home studio\r\n",
                                     "PHP - display results of phpinfo() php command\r\n",
                                     "gp - redisplay last photo taken\r\n",
                                     "tp [arg1,arg2,arg3] - take photo with or without 3 parameters\r\n",
                                     "---> arg1 = QUALITY [1,100], arg2 = WIDTH pixels, arg3 = HEIGHT pixels\r\n",                                 
                                     "ma - MEASURE ALL sensor data\r\n",
                                     "cp - measure current CPU temperature in Centigrade\r\n",
                                     "fl arg1 - flash Arduino onboard led arg1 (within [0,9]) times\r\n",
                                     "ra - Reset/reboot Arduino\r\n",
                                     "st - Test the serial Raspberry PI to Arduino link\r\n",
                                     "pb - Press the wifi dongle button for 6 seconds (for testing servo)\r\n",
                                     "rw - Press the wifi dongle button for 10 seconds to turn it off\r\n",
                                     "---> and then turn it back on in 5 minutes\r\n", 
                                     "sh arg1 - run shell script named arg1 with no arguments\r\n",
                                     "---> reboot\r\n"
                                     "---> with @ = 0 or 1 have scripts\r\n",
                                     "-----> led@_heartbeat\r\n",
                                     "-----> led@_off\r\n",
                                     "-----> led@_on\r\n",
                                     "-----> led@_timer\r\n",
                                     "-----> led@_timer_100\r\n",
                                     "-----> led@_timer_500\r\n",
                                     "-----> led@_timer_2000\r\n",
                                     "pn arg1...arg7- find 1st solution (if any) to numbers game (from Letters & Numbers TV show)\r\n",
                                     "---> arg1 to arg6 are the six used numbers, while arg7 is the sought for solution\r\n",                                     
                                     "dr arg1 - set digital relay off (arg1=o) or on (arg1=-)\r\n"
                                  ])
                    f.close()

                elif (sBodyArg[0] == 'gd'):
                    # meaning: enable link to current sensor data file
                    f = open('/var/tmp/result.txt','w')
                    f.writelines([tx,"Download link to "])
                    f.close()

                elif (sBodyArg[0].upper() == 'LDG'):
                    # meaning: display photo of Lidia Duda-Groblicka in her home studio
                    # the client will be able to download it from the website

                    f = open('/var/tmp/result.txt','w')
                    f.writelines([tx,"Photo of Lidia Duda-Groblicka in studio"])
                    f.close()

                elif (sBodyArg[0].upper() == 'PHP'):
                    # meaning: display results of phpinfo() php command

                    f = open('/var/tmp/result.txt','w')
                    f.writelines([tx,"phpinfo()"])
                    f.close()

                elif (sBodyArg[0] == 'gp'):
                    # meaning: redisplay last photo taken
                    f = open('/var/tmp/result.txt','w')
                    f.writelines([tx,"Display last photo taken"])
                    f.close()

                elif (sBodyArg[0] == 'tp'):
                    # meaning: take photo with or without parameters
                    # the client will be able to download it from the website

                    #run script which takes photo
                    shellscript = 'take_photo_arg'

                    if len(sBodyArg)!=4:
                        #if there are not 3 arguments (not including script name) then just assign default values
                        outstr = RunShellScript_arg(shellscript,75,1024,768)
                    else:
                        # 3 parameters as required by shell script
                        outstr = RunShellScript_arg(shellscript,sBodyArg[1],sBodyArg[2],sBodyArg[3])

                    f = open('/var/tmp/result.txt','w')
                    f.writelines([tx,"Took photo"])
                    f.close()

                elif (sBodyArg[0] == 'ma'):
                    # meaning: measure temperature, pressure, humidity,
                    # rainfall, windspeed, wind direction, current,
                    # voltage and power used by this IOT unit and send it back
                    # to client as text
                    # send serial message (char u) to Arduino Mega

                    while bSerial:
                        time.sleep(2.0)
                    bSerial = True
                    ser.write(b'u')
                    time.sleep(4.0) # to give time for serial reply from Arduino
                    te, pr, hu, rf, ws, wd, cu, bv, po = str(ser.read_until(b'\r\n'))[2:-5].split( )
                    te = str('{:.1f}'.format(round(float(te),1))) # temperature in C 1dp
                    pr = str('{:.1f}'.format(round(float(pr),1))) # pressure in hPa 1dp
                    hu = str('{:.1f}'.format(round(float(hu),1))) # humidity in % 1dp
                    rf = str('{:.1f}'.format(round(float(rf),1))) # rain in mm idp
                    ws = str('{:.1f}'.format(round(float(ws),1))) # wind speed in km/hr 1dp
                    wd = str('{:.1f}'.format(round(float(wd),1))) # wind direction in degrees 1dp
                    cu = str('{:.3f}'.format(round(float(cu)/1000.0,3))) # current in A 3dp
                    bv = str('{:.2f}'.format(round(float(bv)/1000.0,2))) # Bus Voltage in V 2dp
                    po = str('{:.2f}'.format(round(float(po)/1000.0,2))) # power in W 2dp
                    bSerial = False
                    print(te,pr,hu,rf,ws,wd,cu,bv,po," ")

                    f = open('/var/tmp/result.txt','w')
                    f.writelines([tx,"Temperature (C):         "+te,"\r\n",
                                     "Pressure (hPa):          "+pr,"\r\n",
                                     "Humidity (%):            "+hu,"\r\n",
                                     "Rainfall (mm):           "+rf,"\r\n",
                                     "Wind speed (km/hr):      "+ws,"\r\n",
                                     "Wind direction (degrees):"+wd,"\r\n",
                                     "Current (A):             "+cu,"\r\n",
                                     "Bus Voltage (V):         "+bv,"\r\n",
                                     "Power (W):               "+po,"\r\n"])
                    
                    f.close()

                elif (sBodyArg[0] == 'cp'):
                    # meaning: measure current CPU temperature in Centigrade and send it back to client as text

                    # collect CPU temperature via running special script
                    shellscript = 'cputemp'
                    outstr = RunShellScript(shellscript)
                    tCPU = str('{:.1f}'.format(round(float(outstr.strip())/1000.0,1)))

                    f = open('/var/tmp/result.txt','w')
                    f.writelines([tx,"CPU Temperature (C): "+tCPU])
                    f.close()

                elif (sBodyArg[0] == 'fl'):
                    # meaning: flash RPi onboard led sBodyArg[1] (within [2,9]) times
                    print('Flash Led')
                    print(sBodyArg[1])

                    while bSerial:
                        time.sleep(1.0)
                    bSerial = True
                    ser.write(b'f'+sBodyArg[1].encode())
                    bSerial = False

                    f = open('/var/tmp/result.txt','w')
                    f.writelines([tx,"Flashed Arduino onboard led "+sBodyArg[1]+" times"])
                    f.close()

                elif (sBodyArg[0] == 'sh'):
                    # run shell script with name sBodyArg[1] and no arguments
                    print('Run script')
                    print(sBodyArg[0])
                    RunShellScript(sBodyArg[1])

                    f = open('/var/tmp/result.txt','w')
                    f.writelines([tx,"Ran RPi shell script "+sBodyArg[1]+".sh"])
                    f.close()

                elif (sBodyArg[0] == 'pn'):
                    # meaning: find 1st solution (if any) to numbers game (from Letters & Numbers TV show)
                    # the client will see 1st solution on website

                    #run script which searches for solution
                    shellscript = 'numbers_solution'

                    if len(sBodyArg)!=8:
                        #if there are not 7 arguments (not including script name) then just assign default values
                        outstr = RunShellScript_arg7(shellscript,100,75,50,25,10,3,666)
                    else:
                        # 7 parameters as required by shell script
                        outstr = RunShellScript_arg7(shellscript,sBodyArg[1],sBodyArg[2],sBodyArg[3],sBodyArg[4],sBodyArg[5],sBodyArg[6],sBodyArg[7])
                    print(outstr)

                    f = open('/var/tmp/result.txt','w')
                    f.writelines([tx,outstr])
                    f.close()

                elif (sBodyArg[0] == 'dr'):
                    # meaning: set digital relay off or on. "dr o" or "dr -".

                    while bSerial:
                        time.sleep(1.0)
                    bSerial = True
                    f = open('/var/tmp/result.txt','w')
                    sa = sBodyArg[1] # switch argument: o or -
                    if sa == 'o':
                        ser.write(b'y')
                        #wifipower=0
                        msg = "WIFI dongle power OFF"
                    elif sa == '-':
                        ser.write(b'x')
                        #wifipower=1
                        msg = "WIFI dongle power ON"
                    else:
                        msg = "Invalid arguments"
                    print(msg)
                    bSerial = False

                    f.writelines([tx,msg])
                    f.close()

                elif (sBodyArg[0] == 'ra'):
                    # meaning: reboot/reset the Arduino.

                    while bSerial:
                        time.sleep(1.0)
                    bSerial = True
                    f = open('/var/tmp/result.txt','w')
                    ser.write(b'z')
                    msg = "Rebooted/Reset Arduino"
                    print(msg)
                    bSerial = False

                    f.writelines([tx,msg])
                    f.close()

                elif (sBodyArg[0] == 'pb'):
                    # meaning: press the wifi dongle button for 6 seconds.

                    while bSerial:
                        time.sleep(1.0)
                    bSerial = True
                    f = open('/var/tmp/result.txt','w')
                    ser.write(b's')
                    msg = "Pressed the wifi dongle button for 6 seconds"
                    print(msg)
                    bSerial = False

                    f.writelines([tx,msg])
                    f.close()

                elif (sBodyArg[0] == 'st'):
                    # meaning: a serial message test from RPI test to Arduino 

                    while bSerial:
                        time.sleep(1.0)
                    bSerial = True
                    ser.write(b'abcdefghijklmnopabcdefghijklmnopabcdefghijklmnop')
                    time.sleep(1)
                    msg = str(ser.read_until(b'\r\n'))[2:-5]
                    print(msg)
                    bSerial = False

                    f = open('/var/tmp/result.txt','w')
                    f.writelines([tx,msg])
                    f.close()

                elif (sBodyArg[0] == 'rw'):
                    # meaning: press the wifi dongle button for 10 seconds to switch it off and then
                    # after a short time (dtd3) switch it on again (in different code)

                    while bSerial:
                        time.sleep(1.0)
                    bSerial = True
                    # f = open('/var/tmp/result.txt','w')
                    ser.write(b'q')
                    msg = "Pressed the wifi dongle button for 10 seconds"
                    print(msg)
                    bSerial = False

                    WIFIactTime = datetime.datetime.now() + dtd3
                    wifiTURN_ON = True # set flag signifying that wifi needs to be turned on (in this loop)

                    #f.writelines([tx,msg])
                    #f.close()

                else:
                    # Not an actionable command
                    print('Non actionable command')

                    f = open('/var/tmp/result.txt','w')
                    f.writelines([tx,"Does nothing"])
                    f.close()

            except IndexError:
                # "Blank" command sent
                print('No command sent')

                f = open('/var/tmp/result.txt','w')
                f.writelines([tx,"No command sent"])
                f.close()

except KeyboardInterrupt:
    k = k+1
