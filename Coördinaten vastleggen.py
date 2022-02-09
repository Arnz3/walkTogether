import csv
import time
import os
from ublox_gps import UbloxGps
import serial
port = serial.Serial('/dev/serial0', baudrate=38400, timeout=1)
gps = UbloxGps(port)
import RPi.GPIO as GPIO
import sys
from serial import SerialException

f = open('/home/pi/Downloads/gps/vastgelegde_punten.csv', 'w')
writer =  csv.writer(f)
writer.writerow(['lat', 'lon'])


lon_gps = 0.0
lat_gps = 0.0

def getCurrentLocation():
    print('loc')
    #use global to be able to change these variables
    global lat_gps
    global lon_gps
    geo = gps.geo_coords()
    lat_gps = geo.lat
    lon_gps = geo.lon
    print(geo.lat)
    print(geo.lon)

def leg_punt_vast():
    getCurrentLocation()
    print(lat_gps + lon_gps)
    writer.writerow([lat_gps, lon_gps])
    
def stop():
    f.close()
    exit()

if lon_gps > 51 and lat_gps > 2:
    for i in range (0,10):
        leg_punt_vast()
        time.sleep(60)
    stop()
