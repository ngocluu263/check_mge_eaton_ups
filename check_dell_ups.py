#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import subprocess


def main():
   dell_c = int(get_capacity_dell_ups())

   if dell_c == 100:
      print "OK"
   elif dell_c <= 20:
      print "Send mail"
      print "Shutdown servers"
   else:
      print "NG"


def get_capacity_dell_ups():
  try:
     cmd = ["snmpwalk", "-c", "public", "-v", "1", "172.16.4.71", "1.3.6.1.2.1.33.1.2.4.0","-O", "q", "-O", "v"]
     dell_capacity = subprocess.check_output(cmd, shell=False, stderr=subprocess.STDOUT)
     return dell_capacity.strip('\n')
  except:
     return "error"


def get_capacity_eaton_ups():
  try:
     cmd = ["snmpwalk", "-c", "public", "-v", "1", "172.16.4.71", "1.3.6.1.2.1.33.1.2.4.0","-O", "q", "-O", "v"]
     eaton_capacity = subprocess.check_output(cmd, shell=False, stderr=subprocess.STDOUT)
     return eaton_capacity.strip('\n')
  except:
     return "error"

if __name__ == "__main__":
    main()


