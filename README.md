pilogger
========

Temperature and humidity logger using Raspberry Pi and Exosite

Basics:

Themocouplers using One-wire protocol and/ or Adafruit are connected to a Raspberry Pi, which is programmed to upload
temperatures and/or humidity data to Exosite.com for logging and remote display. Additionally, progams will log minimum and
maximum values every mimnute, emailing and reseting each weekday morning.

Thermocouples:
DS18B20 http://www.adafruit.com/product/374 (For temperatures -55 to 125°C)

THERMOCOUPLE AMPLIFIER MAX31855 BREAKOUT BOARD http://www.adafruit.com/product/269 (For temperatures -200°C to +1350°C)

AM2302 TEMPERATURE AND HUMIDITY SENSOR http://www.adafruit.com/product/393 (For temperatures -40 to 80°C and 0-100% humidity)

Wiring:
All sensors share (in parallel) GPIO #4 data, 3.3v, and ground  with a 4.7k pullup resistor between #4 and 3.3v (although AM2302
performance may improve with separate data pin)











