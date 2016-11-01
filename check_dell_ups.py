#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import subprocess
from libsmtp import *

upsInputVoltage = "1.3.6.1.2.1.33.1.3.3.1.3"
upsCapacity = "1.3.6.1.2.1.33.1.2.4.0"
upsBypassVoltage = "1.3.6.1.2.1.33.1.5.3.1.2"
IP = "172.16.4.71"
community = "public"


def main():
   Capacity = int(get_info_ups(IP, community, upsCapacity))
   InputVoltage = int(get_info_ups(IP, community, upsInputVoltage))
   BypassVoltage = int(get_info_ups(IP, community, upsBypassVoltage))

   print ("Capacity: %s " % Capacity)
   print ("InputVoltage: %s " % InputVoltage)
   print ("BypassVoltage: %s " % BypassVoltage)

   if Capacity == 100:
      print "OK"
      print "Send mail"
      #send_mail("UPS low capacity", dell_c)
   elif Capacity <= 20:
      print "Send mail"
      #send_mail("UPS low capacity", dell_c)
      print "Shutdown servers"
      print Capacity
   else:
      print "NG"


def get_info_ups(ip, _community, oid):
  try:
     cmd = ["snmpwalk", "-c", ("%s" % _community), "-v", "1", ("%s" % ip), ("%s" % oid), "-O", "q", "-O", "v"]
     dell_capacity = subprocess.check_output(cmd, shell=False, stderr=subprocess.STDOUT)
     return dell_capacity.strip('\n')
  except:
     return "error"


if __name__ == "__main__":
    main()


