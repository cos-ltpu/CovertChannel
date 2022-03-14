from scapy.all import *
from scapy.config import conf
from scapy.layers.inet import IP
import argparse
from scapy.sendrecv import send

conf.use_pcap = True


if __name__ == '__main__':

    client_address = "127.0.0.1"
    client_port = 10000

    print('starting up on ', client_address, ' port ', client_port)
    filter = "udp dst port " + str(client_port) + " and ip dst host " + str(client_address)

    while True:
        data = sniff(filter=filter, count=1, iface="any")
        if not data:
            print("No data")
        else:
            print(data[0][Raw].load)

