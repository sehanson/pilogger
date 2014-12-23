#from Adafruit_DHT
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

# in crontab -e, */10 * * * * sudo python filepath to run every 10 minutes

import urllib
import httplib
import glob
import os
import subprocess
import time
import sys
import Adafruit_DHT
import decimal
url = '/api:v1/stack/alias'

# connect thermocouples and find addresses to enter below
device_file1 = '/sys/bus/w1/devices/#address#/w1_slave' #Ultralow freezer THERMOCOUPLE AMPLIFIER MAX31855 BREAKOUT BOARD
device_file2 = '/sys/bus/w1/devices/#address#/w1_slave' #Refrigerator DS18B20
sensor = Adafruit_DHT.AM2302 #AM2302 TEMPERATURE AND HUMIDITY SENSOR
pin = 4
humidity, temperature = Adafruit_DHT.read_retry(sensor,pin)


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
   if ambC != 0:
    return ambC
    break
   else:
    time.sleep(1)
    
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
   if ambC2 != 0:
    return ambC2
    break
   else:
    time.sleep(1)

def read_temp3():
 humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
 if humidity is not None and temperature is not None:  
  print 'Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity)
        ambC4=temperature
        rh=humidity
        return ambC4
 else:
        print 'Failed to get reading. Try again!'

def read_rh():
  humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
  if humidity is not None and temperature is not None and  temperature >= 15:
        print 'Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity)
        rh=humidity
        return rh
  else:
        print 'Failed to get reading. Try again!'

cik= 'xxxxxxxxx'#copy and paste cik from Exosite
a= read_temp1()
c= read_temp2()
d= read_temp3()
e= read_rh()
aa=decimal.Decimal(a)
a=round(aa,1)
cc=decimal.Decimal(c)
c=round(cc,1)
if d is not None:
 dd=decimal.Decimal(d)
 d=round(dd,1)
if e is not None:
 ee=decimal.Decimal(e)
 e=round(ee,1)
print (a)
print (c)
print (d)
print (e)
if a!=0 and (-90<a<-10):
 ambC=a
if c!=0 and (-10<c<20):
 ambC2=c
if d!=0 and (15<d<40) and e is not None:
 ambC3 = d
 
while True:
  params = urllib.urlencode({'RH':e, 'RT':d,'FREEZER':ambC,'REFRIGERATOR':ambC3}) #Replace with Data names from Exosite
  headers = {'X-Exosite-CIK':cik,'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8'}
  conn = httplib.HTTPConnection('m2.exosite.com')
  conn.request("POST",url,params,headers)
  response = conn.getresponse();
  print 'POST', url,headers,params
  print 'response:',response.status,response.reason
  data = response.read()
  end = data.find('<')
  if -1 == end: end = len(data)
  print data[:end] #You should get "204: No Content if successful" 
  conn.close()
  break
 else:
  humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
  if humidity is not None and temperature is not None and temperature >14 and humidity > 14:
   dd=decimal.Decimal(temperature)
   d=round(dd,1)
   ee=decimal.Decimal(humidity)
   e=round(ee,1)
