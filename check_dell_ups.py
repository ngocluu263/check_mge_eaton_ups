#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import subprocess
import paramiko
import socket
from libsmtp import *

upsInputVoltage = "1.3.6.1.2.1.33.1.3.3.1.3.1"
upsOutputVoltage = "1.3.6.1.2.1.33.1.4.4.1.2.1"
upsCapacity = "1.3.6.1.2.1.33.1.2.4.0"
upsBatteryLoad = "1.3.6.1.2.1.33.1.2.4.0"
IP = "172.16.4.71"
IP_Target = "172.16.4.93"
USER_Target = "pi"
PASS_Target = "raspberry"
community = "public"


def main():

   InputVoltage = int(get_info_ups(IP, community, upsInputVoltage))
   OutputVoltage = int(get_info_ups(IP, community, upsOutputVoltage))
   Capacity = int(get_info_ups(IP, community, upsCapacity))
   BatteryLoad = int(get_info_ups(IP, community, upsBatteryLoad))

   print ("Capacity: %s " % Capacity)
   print ("InputVoltage: %s " % InputVoltage)
   print ("OutputVoltage: %s " % OutputVoltage)
   print ("BatteryLoad: %s " % BatteryLoad)

   if Capacity == 100:
      print "OK"
      print "Send mail"
      command = "ls"
      output = run_command(IP_Target, USER_Target, PASS_Target, command)
      print output
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


def run_command(server, username, password, command):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(server,username=username, password=password)
            print "Connected to %s." % server
        except (paramiko.SSHException, socket.error):
            print "Failed to connect to %s." % server
            result_failed = ("Failed to connect to %s." % server)
            return result_failed
        stdin, stdout, stderr = ssh.exec_command(command)
        return stdout.readlines()
    except Exception, e:
        print "Couldn't connect to %s, %s" % (server, e)
        result_failed = ("Couldn't connect to %s, %s" % (server, e))
        return result_failed


if __name__ == "__main__":
    main()


