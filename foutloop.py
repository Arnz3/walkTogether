import math
import time

lat1 = 51.072640
lon1 = 2.661655

lat2 = 51.072716
lon2 = 2.662435

foutloop_treshold = 1


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

print(distance(lat1, lon1, lat2, lon2))
        

while True:
    previous_distance = 9999999999999999 
    current_distance = distance()
    print("alles goed")
    if previous_distance - current_distance < foutloop_treshold:
        print("ik denk dat ik fout loop")
        wrong = True    
        startTime = time.time()
        while wrong:
            if startTime - time.time() > 3 and wrong == True:
                print("Ik loop fout")
            if previous_distance - current_distance > foutloop_treshold:
                wrong = False
                print("tis weer")
                break
    previous_distance = current_distance


        

        