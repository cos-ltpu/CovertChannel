import socket
import sys

def eva(data, k):
    msg = ''
    L = 40
    n = 4
    alpha = {0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9'}

    numb = int(len(data)/n)
    msg = alpha.get(numb)
    k = k + 1

    return msg, k

if __name__ == '__main__':
    k = 0

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_address = ('localhost', 9000)
    print('starting up on {} port {}'.format(*client_address))
    sock.bind(client_address)

    # Connect the socket to the port where the server is listening
    server_address = ('localhost', 8000)
    print('connecting to {} port {}'.format(*server_address))
    sock.connect(server_address)

    while True:
        sock.settimeout(100)
        try:
            while True:
                data = sock.recv(256)
                if not data:
                    print("No data")
                else:
                    msg, k = eva(data, k)
                    print('received {!r}'.format(data))
                    print('msg', msg)


        finally:
            print('closing socket')
            sock.close()
