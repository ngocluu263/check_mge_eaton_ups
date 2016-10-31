#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import optparse
import sys

from pysnmp.entity.rfc3413.oneliner import cmdgen


def serviceOID(service):
	# switch servicename to OID
	# define default values
	oidservice	= "undefined"
	minvalue	= "0"
	maxvalue	= "0"
	failurecode	= "0"
	statusmsg	= "undefined"

	# servicename, oid, min- and maxvalues, failurecode and error message
	service2oid = {('battery_remainingtime'):{'oid':'1.3.6.1.4.1.705.1.5.1.0', 'min':1200, 'statusmsg':'Battery Remainingtime under 20min'},
		('battery_level'):{'oid':'1.3.6.1.2.1.33.1.2.4.0', 'min':60, 'statusmsg':'Battery level under 60 percent'},
		('battery_voltage'):{'oid':'1.3.6.1.4.1.705.1.5.2.0', 'min':60, 'statusmsg':'Battery Voltage under 60V'},
		('output_load'):{'oid':'1.3.6.1.4.1.705.1.7.2.1.4.1', 'max':95, 'statusmsg':'Output overload'}
	}

	# get values from dictionary
	if service2oid.has_key(service):
		if service2oid[service].has_key('oid'):
			oidservice	= service2oid[service]['oid']
		if service2oid[service].has_key('min'):
			minvalue	= service2oid[service]['min']
		if service2oid[service].has_key('max'):
			maxvalue	= service2oid[service]['max']
		if service2oid[service].has_key('failure'):
			failurecode	= service2oid[service]['failure']
		if service2oid[service].has_key('statusmsg'):
			statusmsg	= service2oid[service]['statusmsg']

	return(oidservice, minvalue, maxvalue, failurecode, statusmsg)


def getSNMP(ip, community, service):
	# get data from snmpbulkwalk via pysnmp
	snmpwalk	= cmdgen.CommandGenerator()
	errorIndication, errorStatus, errorIndex, varBindTable = snmpwalk.bulkCmd(
		cmdgen.CommunityData(community),
		cmdgen.UdpTransportTarget((ip, 161)),
		0, 25,'1.3.6.1.4.1.705.1.7','1.3.6.1.4.1.705.1.1',)

	# get OID from servicename for switch case
	getOID, getMinvalue, getMaxvalue, getFailurecode, getStatusmsg = serviceOID(service)

	# compare called service OID with snmpwalk
	if errorIndication:
		nagiosOutput(2, "Host %s not available." % ip)
	else:
		if errorStatus:
			nagiosOutput(3, "undefined output")
		else:
			# get all information from destination
			for varBindTableRow in varBindTable:
				for name, val in varBindTableRow:
					#print('%s = %s' % (name.prettyPrint(), val.prettyPrint()))
					snmpName	= name.prettyPrint()
					snmpValue	= val.prettyPrint()

					if(snmpName == getOID):
						# call check
						checkOID(service, getMinvalue, getMaxvalue, getFailurecode, getStatusmsg, snmpValue)


def checkOID(service, minvalue, maxvalue, failurecode, statusmsg, liveval):
	# all Checks
	# convert to int
	getMinvalue		= int(minvalue)
	getMaxvalue		= int(maxvalue)
	getFailurecode	= int(failurecode)
	try:
		getLiveval		= int(liveval)
	except Exception, msg:
		# Liveval is a string
		getLiveval		= liveval
		raise

	# switch case services
	if(service == "battery_level"):
		# Check battery level
		if(getLiveval < getMinvalue):
			# Battery level under Minvalue
			nagiosOutput(2, "Batterylevel: %s" % liveval + "% - " + statusmsg + " | battery_level=%s" % getLiveval+ "%")
		else:
			# Battery level ok
			nagiosOutput(0, "Batterylevel: %s" % liveval + "%" + " | battery_level=%s" % getLiveval + "%")

	elif(service == "battery_remainingtime"):
		# Check battery remaining time
		remaining_minutes	= (getLiveval/60)
		if(getLiveval < getMinvalue):
			# Battery remainingtime under Minvalue
			nagiosOutput(2, "Battery remainingtime: %s" % liveval + "s (%s" % remaining_minutes + "min) - " + statusmsg + " | battery_remainingtime=%s" % getLiveval + "s")
		else:
			# Battery remainingtime ok
			nagiosOutput(0, "Battery remainingtime: %s" % liveval + "s (%s" % remaining_minutes + "min)" + " | battery_remainingtime=%s" % getLiveval + "s")

	elif(service == "battery_voltage"):
		# Check Battery Voltage
		batteryVoltage	= (getLiveval/10)
		if(getLiveval < getMinvalue):
			# Battery remainingtime under Minvalue
			nagiosOutput(2, "Battery voltage: %s" % getLiveval + "V - " + statusmsg + " | battery_voltage=%s" % getLiveval + "%")
		else:
			# Battery remainingtime ok
			nagiosOutput(0, "Battery voltage: %s" % getLiveval + "V" + " | battery_voltage=%s" % getLiveval + "%")

	elif(service == "output_load"):
		# Check output load
		if(getLiveval > getMaxvalue):
			# Battery overload
			nagiosOutput(2, "Battery output load: %s" % getLiveval + "% - " + statusmsg + " | battery_output_load=%s" % getLiveval + "%")
		else:
			# Battery remainingtime ok
			nagiosOutput(0, "Battery output load: %s" % getLiveval + "%" + " | battery_output_load=%s" % getLiveval + "%")




def nagiosOutput(status, message):
	# Create output for nagios
	if(status==0):
		state	= "OK"
	elif(status==1):
		state	= "WARN"
	elif(status==2):
		state	= "CRIT"
	elif(status==3):
		state	="UNKN"
	else:
		state	="UNKN"
		message	="status is not defined"

	sys.stdout.write(state + ": " + message + "\n")
	sys.exit(status)


def main():
	# Starting check_mge_eaton_ups.py
	parser = optparse.OptionParser()
	parser.add_option("-c", "--community", dest="community", help="configured community [default: public]", default=False)
	parser.add_option("-H", "--host", dest="host", help="IP of destination", default=False)
	parser.add_option("-o", "--option", dest="option", help="""Choose option (OID) to check:
		battery_remainingtime
		battery_level
		battery_voltage
		battery_chargerfault
		battery_low_condition
		input_voltage
		input_frequency
		input_line_fail_cause
		input_bad_status
		output_load
		output_voltage
		output_frequency
		output_on_battery
		output_on_by_pass
		output_overload
		output_inverter_off
		ambient_temperature
		""", default=False)
	(options, args) = parser.parse_args()  # pylint: disable=W0612

	try:
		#if options.help:
			# print help
		#	print("HELP")

		if options.community is False:
			# no community set, use default
			options.community	= "public"

		if options.host is False:
			# no destination set, exit
			nagiosOutput(3, "No destination IP is set.")

		if options.option is False:
			# no service is set, exit
			nagiosOutput(3, "No service is choosen. For help -h")

		print getSNMP(options.host, options.community, options.option)

	except IOError, msg:
		nagiosOutput(3, "IOError")
		raise
	except Exception, msg:
		nagiosOutput(3, "Exception")
		raise


if __name__ == "__main__":
		main()


