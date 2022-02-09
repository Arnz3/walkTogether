from bluepy.btle import *

Lband_addr ="e7:0c:02:89:d7:a8"
Rband_addr ="c1:2f:54:e1:60:98"

svc_uuid ="AAE28F00-71B5-42A1-8C3C-F9CF6AC969D0"
ch_uuid ="AAE28F02-71B5-42A1-8C3C-F9CF6AC969D0"

p = Peripheral(Lband_addr,ADDR_TYPE_RANDOM)
svc = p.getServiceByUUID(svc_uuid)
ch = svc.getCharacteristics(ch_uuid)[0]

ch.write(vib1sec)