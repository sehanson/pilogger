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

Python programs used:
ExositeUpload - Runs every 10 minutes through cron, uploads temperature readings to Portals.exosite.com
MinMax - Runs every 1 minute through cron, opens text files which have recorded in each the minimum or maximum temperture for that sensor since the last email.
Email - Runs every weekeday at 8AM through cron, opens text files for the minuimum and maximum values since the last email and sends an email with these values. It then writes the current value as both the minimum and maximum.

Thermocouple IDs:
Actual thermocouple ID numbers are written into the programs in order to differentiate sources. 










