#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import optparse
import sys

from pysnmp.entity.rfc3413.oneliner import cmdgen

from pysnmp.hlapi import *

def main():

	try:
			# Starting check_mge_eaton_ups.py
		iterator = getCmd(SnmpEngine(),
						  CommunityData('public'),
						  UdpTransportTarget(('172.16.4.71', 161)),
						  ContextData(),
						  ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysDescr', 0)))

		errorIndication, errorStatus, errorIndex, varBinds = next(iterator)

		if errorIndication:  # SNMP engine errors
			print(errorIndication)
		else:
			if errorStatus:  # SNMP agent errors
				print('%s at %s' % (errorStatus.prettyPrint(), varBinds[int(errorIndex)-1] if errorIndex else '?'))
			else:
				for varBind in varBinds:  # SNMP response contents
					print(' = '.join([x.prettyPrint() for x in varBind]))

	except IOError, msg:
		nagiosOutput(3, "IOError")
		raise
	except Exception, msg:
		nagiosOutput(3, "Exception")
		raise


if __name__ == "__main__":
		main()


