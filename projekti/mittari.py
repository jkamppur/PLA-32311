
#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

# Huoneilmanlaadun dataloggeri Juha Kamppuri 262582

import Adafruit_DHT
import mh_z19

from datetime import datetime, timedelta
from time import sleep


def get_meas_file_name():
   file_ok = False
   while (file_ok == False):
      name = raw_input("Anna mitattavan huoneen nimi: ")
      if (len(name) > 0):
         file_ok = True
   name = name.replace(" ","_")
   name = name + ".csv"
   print("Tulokset tallentaan tiedostoon " + name)

   return name


def main():
   # DHT11 sensori
   dht11_sensor=Adafruit_DHT.DHT11
   dht11_gpio=17

   sleep_time = 120

   file_name = get_meas_file_name()
   meas_time = raw_input("Anna mittauksen aika tunteina: ")

   # Time to stop measure
   timestamp_start = datetime.now()
   timestamp_end = timestamp_start + timedelta(hours=int(meas_time))

   # open file for results
   file = open(file_name,"w")   
   file.write('date, time, temperature, humidity, co2\r\n')


   while True:

      # debug
      hum = 10
      temp = 20
      co2 = 400

      # read dht11 sensor
      hum, temp = Adafruit_DHT.read_retry(dht11_sensor, dht11_gpio)    

      # read MH_Z19 sensor
      co2 = mh_z19.read()["co2"]
      
      timestamp_now = datetime.now()
      time_left = int((timestamp_end - timestamp_now).total_seconds() / 60.0)
        

      # print data to screen and file
      time = datetime.now().strftime('%Y-%m-%d %H:%M')
      print('{3}  Temp={0:0.1f}*C  Humidity={1:0.1f}%  CO2={2}ppm  time left (minutes)={4}'.format(temp, hum, co2, time, time_left))
      time = datetime.now().strftime('%Y-%m-%d, %H:%M')


      #temp = int(temp)
      #hum = int(hum)
      file.write('{0},{1},{2},{3}\r\n'.format(time, int(temp), int(hum), co2))

      # Check if time to quit      
      if (timestamp_now > timestamp_end):
         break

      # break before next round
      sleep(sleep_time)

   file.close

main()