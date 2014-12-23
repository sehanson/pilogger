#from Adaruit_DHT
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

device_file1 = '/sys/bus/w1/devices/#address#/w1_slave' #-70
device_file2 = '/sys/bus/w1/devices/#address#/w1_slave' #4c
#device_file3 = '/sys/bus/w1/devices/#address#/w1_slave' #rt
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
 while True:
  lines= read_temp_raw1()
  while lines[0].strip()[-3:]!='YES':
   time.sleep(1)
   lines = read_temp_raw1()
  equals_pos = lines[1].find('t=')
  if equals_pos !=-1:
   temp_string = lines[1][equals_pos+2:]
   ambC = float(temp_string)/1000
   if ambC !=0:
    a = decimal.Decimal(ambC)
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
 while True:
  lines= read_temp_raw2()
  while lines[0].strip()[-3:]!='YES':
   time.sleep(1)
   lines = read_temp_raw2()
  equals_pos = lines[1].find('t=')
  if equals_pos !=-1:
   temp_string = lines[1][equals_pos+2:]
   ambC2 = float(temp_string)/1000
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
  if temperature > 15:
   c = temperature
   cc = decimal.Decimal(c)
   c = round(c,1)
   return c
   break
  else:
   time.sleep(10)

h=str('/home/pi/temps/')
h1=h+name1+'max.txt'
file=open(h1,'r')
name1min=file.read()
file.close()
time.sleep(1)
h2=h+name1+'max.txt'
file=open(h2, 'r')
name1max=file.read()
file.close()
time.sleep(1)
h3=h+name2+'max.txt'
file=open(h3,'r')
name2max=file.read()
file.close()
time.sleep(1)
h4=h+name2+'min.txt'
file=open(h4, 'r')
name2min=file.read()
file.close()
time.sleep(1)
h5=h+name3+'min.txt'
file=open(h5,'r')
name3min=file.read()
file.close()
time.sleep(1)
h6=h+name3+'max.txt'
file=open(h6, 'r')
name3max=file.read()
file.close()
time.sleep(1)

a= read_temp1()
b= read_temp2()
c= read_temp3()

if a<float(name1min) and (-90<a<-1): #make sure temps are within a typical range to avoid a random bad read
        ambC=a
        name1min=str(ambC)
        file=open(h1,'w')
        file.write(name1min)
        file.close()
if a>float(name1max) and (-90<a<-1):
        ambC = a
        name1max=str(ambC)
        file=open(h2,'w')
        file.write(name1max)
        file.close()
if b<float(name2min) and (-5<b<15):
        ambC2 = b
        name2min=str(ambC2)
        file=open(h4,'w')
        file.write(name2min)
        file.close()
if b>float(name2max) and (-5<b<15):
        ambC2 = b
        name2max=str(ambC2)
        file=open(h3,'w')
        file.write(name2max)
        file.close()
if c<float(name3min)and c != 0 and (15<c<50):
        ambC3=c
        name3min=str(ambC3)
        file=open(h5,'w')
        file.write(name3min)
        file.close()
if c>float(name3max) and c != 0 and (15<c<50):
        ambC3=c
        name3max=str(ambC3)
        file=open(h6,'w')
        file.write(name3max)
        file.close()
print (a)
print (c)
print (b)



