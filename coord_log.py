from curses import baudrate
import serial
from ublox_gps import UbloxGps

port = serial.Serial('/dev/ttyACM0', baudrate=38400, timeout=1)
gps = UbloxGps(port)

nrml_lat = 2
nrml_lon = 51

while True:
    geo = gps.geo_coords()
    lat = str(geo.lat)
    lon = str(geo.lon)

    if int(lat.split('.')[0]) == nrml_lat and int(lon.split('.')[1]) == nrml_lon:
        print(lat + " , " + lon + " > gecallibreerd")

    else:
        print(lat + " , " + lon + " > niet gecallibreerd")
        
