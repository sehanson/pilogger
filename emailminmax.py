#from adafruit_DHT
#The MIT License (MIT)

#Copyright (c) 2014 Adafruit Industries

#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.



import urllib
import httplib
import glob
import os
import subprocess
import time
import smtplib
import socket
from email.mime.text import MIMEText
import datetime
import sys
import Adafruit_DHT
import decimal

url = '/api:v1/stack/alias'

device_file1 = '/sys/bus/w1/devices/3b-00000018259a/w1_slave' #-70
device_file2 = '/sys/bus/w1/devices/28-0000034d323d/w1_slave' #4c
#device_file3 = '/sys/bus/w1/devices/28-0000034cfa04/w1_slave' #rt
sensor = Adafruit_DHT.AM2302
pin = 4

room="M764"
name1='Freezer_8'
name2='Refrigerator'
name3='Room_Temp'


def read_temp_raw1():
 f = open(device_file1, 'r')
 lines = f.readlines()
 f.close()
 return lines

def read_temp1():
  lines= read_temp_raw1()
  while lines[0].strip()[-3:]!='YES':
   time.sleep(1)
   lines = read_temp_raw1()
  equals_pos = lines[1].find('t=')
  if equals_pos !=-1:
   temp_string = lines[1][equals_pos+2:]
   ambC = float(temp_string)/1000
   return ambC

def read_temp11():
 while True:
  ambC = read_temp1()
  if ambC !=0:
   a=decimal.Decimal(ambC)
   ambC = round(a,1)
   return ambC
   break
  else:
   time.sleep(2)

def read_temp_raw2():
 f = open(device_file2, 'r')
 lines = f.readlines()
 f.close()
 return lines

def read_temp2():
  lines= read_temp_raw2()
  while lines[0].strip()[-3:]!='YES':
   time.sleep(1)
   lines = read_temp_raw2()
  equals_pos = lines[1].find('t=')
  if equals_pos !=-1:
   temp_string = lines[1][equals_pos+2:]
   ambC2 = float(temp_string)/1000
   return ambC2

def read_temp22():
 while True:
  ambC2 = read_temp2()
  if ambC2 !=0:
   a=decimal.Decimal(ambC2)
   ambC2 = round(a,1)
   return ambC2
   break
  else:
   time.sleep(2)


def read_temp3():
 while True:
  humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
  if temperature is not None and temperature > 15:
   return temperature
  else:
   time.sleep(3)

h=str('/home/pi/temps/')
h1=h+name1+'min.txt'
file=open(h1,'r')
name1min=file.read()
file.close()
h2=h+name1+'max.txt'
file=open(h2, 'r')
name1max=file.read()
file.close()
h3=h+name2+'max.txt'
file=open(h3,'r')
name2max=file.read()
file.close()
h4=h+name2+'min.txt'
file=open(h4, 'r')
name2min=file.read()
file.close()
h5=h+name3+'min.txt'
file=open(h5,'r')
name3min=file.read()
file.close()
h6=h+name3+'max.txt'
file=open(h6, 'r')
name3max=file.read()
file.close()




while True:
 a= read_temp11()
 b= read_temp22()
 c= read_temp3()

 if c is not None:
  cc=decimal.Decimal(c)
  c=round(cc,2)
 else:
  c=(RTmin+RTmax)/2
 print (a)
 print (b)
 print (c)


 D=int(datetime.date.today().strftime('%w'))
 H=int(datetime.datetime.now().strftime('%H'))
 M=int(datetime.datetime.now().strftime('%M'))

# Change to your own account information
 to = ""#enter email address
 gmail_user = '@gmail.com' #enter your gmail user name
 gmail_password = '' #enter your gmail password
 smtpserver = smtplib.SMTP('smtp.gmail.com', 587)
 smtpserver.ehlo()
 smtpserver.starttls()
 smtpserver.ehlo
 smtpserver.login(gmail_user, gmail_password)
 today = datetime.date.today()
#        Very Linux Specific
 arg='ip route list'
 p=subprocess.Popen(arg,shell=True,stdout=subprocess.PIPE)
 data = p.communicate()
 split_data = data[0].split()
 ipaddr = split_data[split_data.index('src')+1]
 while ipaddr: #if connection is down this will loop until it returns
  mail_body = room + " "+ name1 + " Min= " + name1min + "C Max= " + name1max + 'C\n' + room + " "+name2 +' Min= '+ name2min + 'C Max= '+name2max + 'C\n'+room+" "+name3+ ' Min= ' + name3min + 'C Max= '+name3max+'C\nIP address:'+ipaddr
  msg = MIMEText(mail_body)
  msg['Subject'] = room +' Temp Records for %s'% today.strftime('%b %d %Y')
  msg['From'] = gmail_user
  msg['To'] = to
  smtpserver.sendmail(gmail_user, [to], msg.as_string())
  smtpserver.quit()
  name1min=str(a)
  file=open(h1,'w')
  file.write(name1min)
  file.close()
  name1max=str(a)
  file=open(h2,'w')
  file.write(name1max)
  file.close()
  name2min=str(b)
  file=open(h4,'w')
  file.write(name2min)
  file.close()
  name2max=str(b)
  file=open(h3,'w')
  file.write(name2max)
  file.close()
  name3min=str(c)
  file=open(h5,'w')
  file.write(name3min)
  file.close()
  name3max=str(c)
  file=open(h6,'w')
  file.write(name3max)
  file.close()
  break
 else:
  time.sleep(60)
 break
