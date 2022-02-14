import csv
import time
from ublox_gps import UbloxGps
import serial
from datetime import datetime
import RPi.GPIO as GPIO
port = serial.Serial('/dev/serial0', baudrate=38400, timeout=1)
gps = UbloxGps(port)

f = open('docs/', 'w')
writer =  csv.writer(f)
writer.writerow(['lat', 'lon', 'time'])
GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.IN)

lon_gps = 0.0
lat_gps = 0.0

run = True
waitTime = 3

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
    time = datetime.now().strftime("%H:%M:%S")
    writer.writerow([lat_gps, lon_gps, time])


def stop():
    f.close()
    exit()


def checkHalt():
    if(GPIO.input(21)):
        stop()


while run:
    leg_punt_vast()
    checkHalt()
    time.sleep(waitTime)