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
    # assume min gap divides 60 minutes in hour ie is (1,2,4,5,6,10,12,15,20,30,60)
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


n=0

# gap in minutes between data collection events (assume 60 % minGap == 0)
minGap = 5

# data collection time gap
dtd = datetime.timedelta(days=0,hours=0,minutes=minGap,seconds=0)

#initial future time at which we will start collecting data
actTime = CollectDataStartTime(minGap)

# when first started do this to avoid spurious client command
shutil.copyfile('/var/tmp/text.txt','/var/tmp/text_bak.txt')

        
try:
    while True:
        dtn = datetime.datetime.now()
        dtns = dtn.strftime('%d%b%Y-%H:%M:%S')
        tx = dtn.strftime('%H%M%S')+"\r\n"
        dtnt = dtn.time() # the time of now (ignores date)

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

        # Append collected data to data file with a time stamp
            odf = open('/var/www/html/SensorData.csv','a',newline='')
            odw = csv.writer(odf)
            odw.writerow([ats, tCPU])
            odf.close()

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
                                     "PHP - display results of phpinfo() php command\r\n",
                                     "gp - redisplay last photo taken\r\n",
                                     "tp - take photo with or without parameters\r\n", 
                                     "cp - measure current CPU temperature in Centigrade\r\n",
                                     "sh arg1 - run shell script named arg1 with no arguments\r\n",
                                     "---> reboot\r\n"
                                     "---> with # = 0 or 1 have scripts\r\n",
                                     "-----> led#_heartbeat\r\n",
                                     "-----> led#_off\r\n",
                                     "-----> led#_on\r\n"])
                    f.close()
                
                elif (sBodyArg[0] == 'gd'):
                    # meaning: enable link to current sensor data file
                    f = open('/var/tmp/result.txt','w')
                    f.writelines([tx,"Download link to "])
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
 
                elif (sBodyArg[0] == 'cp'):
                    # meaning: measure current CPU temperature in Centigrade and send it back to client as text

                    # collect CPU temperature via running special script
                    shellscript = 'cputemp'
                    outstr = RunShellScript(shellscript)
                    tCPU = str('{:.1f}'.format(round(float(outstr.strip())/1000.0,1)))

                    # crash nginx webserver / restart test
                    RunShellScript('killnginx')

                    # crash / restart python test
                    x = 1.0/0.0
                    print(x)

                    f = open('/var/tmp/result.txt','w')
                    f.writelines([tx,"CPU Temperature (C): "+tCPU])
                    f.close()
 
                elif (sBodyArg[0] == 'sh'):
                    # run shell script with name sBodyArg[1] and no arguments
                    print('Run script')
                    print(sBodyArg[0])
                    RunShellScript(sBodyArg[1])

                    f = open('/var/tmp/result.txt','w')
                    f.writelines([tx,"Ran RPi shell script "+sBodyArg[1]+".sh"])
                    f.close()
  
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
