import csv
import time
import serial
import sys
from ublox_gps import UbloxGps
from bluepy.btle import *
from datetime import datetime


#========= INITIALIZING GPS ========= 

port = serial.Serial('/dev/ttyACM0', baudrate=38400, timeout=1)
gps = UbloxGps(port)


#========= LOCAL VARIABLES ========= 

#MAC address for the smartbands
Lband_addr ="e7:0c:02:89:d7:a8"
Rband_addr ="c1:2f:54:e1:60:98"

# service and Characteristics UUID
svc_uuid ="AAE28F00-71B5-42A1-8C3C-F9CF6AC969D0"
ch_uuid ="AAE28F02-71B5-42A1-8C3C-F9CF6AC969D0"

#data for the vibrations
vib1sec = bytes.fromhex("FF086B016414012E")
vib3sec = bytes.fromhex("FF086B01643C01D6")
vib2x1sec = bytes.fromhex("FF0E6B0264141464141454")

#declare variables
point_number = 1 #number to indicate next waypoint
point_code = 0  #1='crossing road', 2='something to feel', 3='end'
delay_time = 1 

#rough coords the gps should be on
nrml_lat = 51
nrml_lon = 2

#to save coordinates
max_difference = 0.00005 #max difference in lat and lon to be accepted
lon_gps = 0.0
lat_gps = 0.0
lon_csv = 0.0
lat_csv = 0.0
turn_angle = 0.0  #angle that has to be turned on next point
direction = 'L'

dateTime = datetime.now().strftime("%m.%d-%H:%M:%S")

csv_file = csv.reader(open('docs/wandeling.csv')) #read the csv file
csv_list = list(csv_file)   #convert file to list


#========= FUNCTIONS ========= 

def connect():    #connect to smartbands
    global l
    global r 

    try:
        lBand = Peripheral(Lband_addr, ADDR_TYPE_RANDOM)
        rBand = Peripheral(Rband_addr, ADDR_TYPE_RANDOM)
    except:
        print("ERROR: Failed to connect to smartbands!")
        connect()

    #find Characteristics and services
    svcL = lBand.getServiceByUUID(svc_uuid)
    svcR = rBand.getServiceByUUID(svc_uuid)
    l = svcL.getCharacteristics(ch_uuid)[0]
    r = svcR.getCharacteristics(ch_uuid)[0]


def checkCoords():
    geo = gps.geo_coords()
    lat = str(geo.lat)
    lon = str(geo.lon)

    if int(lat.split('.')[0]) == nrml_lat and int(lon.split('.')[0]) == nrml_lon:
        l.write(vib1sec)
        r.write(vib1sec)
        time.sleep(1.5)
        l.write(vib3sec)
        r.write(vib3sec)
        time.sleep(3)

    else:
        checkCoords()


#function to receive and save data from waypoint
def loadPointInfo(number):
    #use global to be able to change these variables
    global point_code
    global lat_csv
    global lon_csv
    global turn_angle
    global direction
    lat_csv = float(csv_list[number][0])
    lon_csv = float(csv_list[number][1])
    direction = str(csv_list[number][2])
    point_code = int(csv_list[number][-1])


#function to receive curren location from gps module
def getCurrentLocation():
    #use global to be able to change these variables
    global lat_gps
    global lon_gps
    geo = gps.geo_coords()
    lat_gps = geo.lat
    lon_gps = geo.lon



def changeToNextPoint():
    #use global to be able to change this variable
    global point_number
    point_number+=1
    loadPointInfo(point_number)


#function to turn on the motor dependend on the angle and direction
def turn(direction):
    for letter in direction:
        if letter.lower() == 'l':
            l.write(vib1sec)
            print("L")
        elif letter.lower() == 'r':
            r.write(vib1sec)
            print("R")
        elif letter.lower() == 'z':
            print("cross")
            l.write(vib2x1sec)
            r.write(vib2x1sec)
        else:
            time.sleep(int(letter))

#function to turn on the motors for a special action
def specialAction(code):
    if code == 1:   # crossing road
        print("cross")
        l.write(vib2x1sec)
        r.write(vib2x1sec)
    if code == 2:   # something to feel
        print("feel")
        l.write(vib3sec)
        l.write(vib3sec)
    if code == 3:   # end of the trip
        print("end")
        for _ in range(3):
            l.write(vib1sec)
            time.sleep(1)
            r.write(vib1sec)
            time.sleep(1)
        sys.exit()


#========= MAIN LOOP ========= 

connect()
checkCoords()   
try:
    loadPointInfo(point_number)
    while True:
        getCurrentLocation()
        print("CSV:      ",lat_csv,",",lon_csv)
        print("Verschil: ",abs(lat_gps-lat_csv),",",abs(lon_gps-lon_csv))
        if abs(lon_gps - lon_csv) < max_difference and abs(lat_gps - lat_csv) < max_difference:
            print("point")
            turn(direction)
            specialAction(point_code)
            print("go to next point")
            changeToNextPoint()
        time.sleep(delay_time)

finally:
    port.close()
