from scapy.all import *
from scapy.config import conf
from scapy.layers.inet import IP
import argparse
from scapy.sendrecv import send

conf.use_pcap = True


def parse_arguments():
    parser = argparse.ArgumentParser(description='Covert channel emulation',
                                        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-L', '--length', help='length of packet',
                        required=True, dest='length', type=int, default=100)
    parser.add_argument('-n', help='number of parts',
                        required=True, dest='numb', type=int, default=10)
    return parser.parse_args()


def eva(data):
    alpha = {0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9'}

    numb = int((len(data)-44)/L*n)
    msg = alpha.get(numb)

    return msg


if __name__ == '__main__':
    args = parse_arguments()
    L = args.length
    n = args.numb

    client_address = "127.0.0.1"
    client_port = 10000

    print('starting up on ', client_address, ' port ', client_port)
    filter = "udp dst port " + str(client_port) + " and ip dst host " + str(client_address)

    while True:
        data = sniff(filter=filter, count=1, iface="any")
        if not data:
            print("No data")
        else:
            msg = eva(data[0])
            print('msg', msg)
