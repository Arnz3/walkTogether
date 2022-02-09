import csv
import time
import os
from ublox_gps import UbloxGps
import serial
port = serial.Serial('/dev/serial0', baudrate=38400, timeout=1)
gps = UbloxGps(port)
import RPi.GPIO as GPIO
import sys

#declare variables for motors
motor_left = 17
motor_right = 27

#initialize the motors
GPIO.setmode(GPIO.BCM)
GPIO.setup(motor_left, GPIO.OUT)
GPIO.setup(motor_right, GPIO.OUT)
GPIO.output(motor_left, 0)
GPIO.output(motor_right, 0)

#declare variables
point_number = 1 #number to indicate next waypoint
point_code = 0  #1='crossing road', 2='something to feel', 3='end'
delay_time = 1

#to save coordinates
max_difference = 0.00005 #max difference in lat and lon to be accepted
lon_gps = 0.0
lat_gps = 0.0
lon_csv = 0.0
lat_csv = 0.0
turn_angle = 0.0  #angle that has to be turned on next point
direction = 'L'

csv_file = csv.reader(open('test_thuis.csv')) #read the csv file
csv_list = list(csv_file)   #convert file to list

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
    turn_angle = float(csv_list[number][3])
    point_code = int(csv_list[number][4])


#function to receive curren location from gps module
def getCurrentLocation():
    #use global to be able to change these variables
    global lat_gps
    global lon_gps
    geo = gps.geo_coords()
    lat_gps = geo.lat
    lon_gps = geo.lon
    print(lat_gps)
    print(lon_gps)


def changeToNextPoint():
    #use global to be able to change this variable
    global point_number
    point_number+=1
    loadPointInfo(point_number)

#function to pulse one of the motors for given times
def vibrate(pin, time_on, times):
    for x in range(0, times):
        GPIO.output(pin, 1)
        time.sleep(time_on)
        GPIO.output(pin, 0)
        time.sleep(time_on)

#function to turn on the motor dependend on the angle and direction
def turn(direction, angle):
    if direction.lower() == 'l':
        control_pin = motor_left
        print("Left")
    else:
        control_pin = motor_right
        print("Right")
    
    if angle == 0:
        return
    elif angle <= 45:
        vibrate(control_pin, 1, 3)
    elif angle <= 90:
        vibrate(control_pin, 0.75, 4)
    elif angle <= 135:
        vibrate(control_pin, 0.5, 5)
    else:
        vibrate(control_pin, 0.25, 10)
    time.sleep(0.5)

#function to turn on the motors for a special action
def specialAction(code):
    if code == 1:   # crossing road
        GPIO.output(motor_left, 1)
        GPIO.output(motor_right, 1)
        time.sleep(2)
        GPIO.output(motor_right, 0)
        GPIO.output(motor_left, 0)
    if code == 2:   # something to feel
        for x in range(0, 2):
            for n in range(0,3):
                GPIO.output(motor_left, 1)
                GPIO.output(motor_right, 1)
                time.sleep(0.2)
                GPIO.output(motor_right, 0)
                GPIO.output(motor_left, 0)
                time.sleep(0.2)
            time.sleep(0.5)
    if code == 3:   # end of the trip
        print("end")
        for x in range(0, 10):
            GPIO.output(motor_left, 1)
            GPIO.output(motor_right, 0)
            time.sleep(0.2)
            GPIO.output(motor_right, 1)
            GPIO.output(motor_left, 0)
            time.sleep(0.2)
        GPIO.output(motor_right, 0)
        GPIO.output(motor_left, 0)
        sys.exit()

try:
    loadPointInfo(point_number)
    while True:
        getCurrentLocation()
        if abs(lon_gps - lon_csv) < max_difference and abs(lat_gps - lat_csv) < max_difference:
            turn(direction, turn_angle)
            specialAction(point_code)
            changeToNextPoint()
        time.sleep(delay_time)

finally:
    port.close()
