import socket
import sys
import time
from scapy.all import *
from scapy.config import conf
from scapy.layers.inet import IP, UDP, ICMP
import argparse

conf.use_pcap = True


def parse_arguments():
    parser = argparse.ArgumentParser(description='Covert channel emulation',
                                        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-L', '--length', help='length of packet',
                        required=True, dest='length', type=int, default=100)
    return parser.parse_args()


if __name__ == '__main__':

    args = parse_arguments()
    L = args.length

    server_address = "127.0.0.1"
    server_port = 9000
    print('starting up on', server_address)

    while True:
        print('waiting for a connection')
        proxy_address = "127.0.0.1"
        proxy_port = 8000
        try:
            print('connection from', proxy_address)
            while True:
                data = "This is the message."
                pkt = IP(dst=proxy_address)/UDP(sport=server_port, dport=proxy_port)
                #L = L - len(pkt)
                if len(data) < L:
                    print('send', data)
                    send(pkt/Raw(data))
                else:
                    for item in [data[i:i + L] for i in range(0, len(data), L)]:
                        print('send1', item)
                        send(pkt / Raw(item))
                time.sleep(10.0)

        finally:
            time.sleep(1)
