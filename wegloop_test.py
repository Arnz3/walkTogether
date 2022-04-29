import time
import math
import csv
from ublox_gps import UbloxGps
import serial
from bluepy.btle import *

port = serSerial('/dev/ttyACM0', baudrate=38400, timeout=1)
gps = UbloxGps(port)

csv_file = csv.reader(open('test_thuis.csv')) #read the csv file
csv_list = list(csv_file)   #convert file to list

foutloop_treshold = 1
delay_time = 1

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


def distance(lat1, lon1, lat2, lon2):
    R = 6371000

    phi1 = lat1 * math.pi/180
    phi2 = lat2 * math.pi/180
    dphi = (lat2-lat1) * math.pi/180
    dlam = (lon2- lon1) * math.pi/180

    a = math.sin(dphi/2) * math.sin(dphi/2) + math.cos(phi1) * math.cos(phi2) * math.sin(dlam/2) * math.sin(dlam/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    d = R * c
    return d 


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
    turn_angle = float(csv_list[number][3])
    point_code = int(csv_list[number][4])


def getCurrentLocation():
    #use global to be able to change these variables
    global lat_gps
    global lon_gps
    geo = gps.geo_coords()
    lat_gps = geo.lat
    lon_gps = geo.lon


loadPointInfo(1)
connect()

previous_distance = 9999999999999999
while True:
    getCurrentLocation()
    current_distance = distance(lat_csv, lon_csv, lat_gps, lon_gps)
    if previous_distance - current_distance < foutloop_treshold:
        wrong = True
        startTime = time.time()
        while wrong:
            getCurrentLocation()
            current_distance = distance(lat_csv, lon_csv, lat_gps, lon_gps)
            if startTime - time.time() > 5 and wrong == True:
                print("ik loop fout")
                l.write(vib1sec)
                r.write(vib1sec)

            if previous_distance - current_distance > foutloop_treshold:
                wrong = False
                break
            time.sleep(delay_time)
            previous_distance = current_distance

    previous_distance = current_distance
    time.sleep(delay_time)