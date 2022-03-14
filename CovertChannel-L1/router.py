import socket
import sys
import random
from scapy.all import *
from scapy.config import conf
from scapy.layers.inet import IP, UDP
from scapy.sendrecv import send
import argparse

conf.use_pcap = True


def parse_arguments():
    parser = argparse.ArgumentParser(description='Covert channel emulation',
                                        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-L', '--length', help='length of packet',
                        required=True, dest='length', type=int, default=100)
    parser.add_argument('-n', help='number of parts',
                        required=True, dest='numb', type=int, default=10)
    parser.add_argument('-s', '--secret', help='string',
                        required=True, dest='str', type=str, default='1234')
    return parser.parse_args()


def eva(secret, data):
    alpha = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9}
    if len(secret) > 0:
        raw_l = len(data)-44
        size = random.randint(alpha.get(secret) * n, (alpha.get(secret) + 1) * n - 1)
        if raw_l >= size:
            data[Raw].load = data[Raw].load[0:size]
        else:
            pad_len = size - raw_l
            pad = Padding()
            pad.load = '\x00' * pad_len
            data = data / pad
    return data


if __name__ == '__main__':

    args = parse_arguments()
    L = args.length
    n = args.numb
    secret = args.str

    proxy_address = "127.0.0.1"
    proxy_port = 8000

    server_address = "127.0.0.1"
    server_port = 9000

    client_address = "127.0.0.1"
    client_port = 10000

    print('starting up on ', proxy_address, ' port ', proxy_port)
    print('connection from', client_address)
    print('connecting to ', server_address, ' port ', server_port)

    while True:
        filter = "udp src port " + str(server_port) + " and ip host " + str(server_address)
        data = sniff(filter = filter, count = 1, iface = "any")
        if not data:
            print("No data")
            break
        else:
            ############
            data = [eva(secret[0], data[0])]
            secret = secret[1:]
            ############
            data = data[0][UDP]
            data.dport = client_port
            send(IP(dst=client_address)/data)