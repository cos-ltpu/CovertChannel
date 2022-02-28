import socket
import sys
import random

def eva(data, k):
    L = 40
    n = 4
    secret = '88005553535'
    alpha = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9}
    if len(secret) > k:
        size = random.randint(alpha.get(secret[k]) * n, (alpha.get(secret[k]) + 1) * n - 1)
        k = k + 1
        if len(data) >= size:
            data = data[0:size]
        else:
            data = data.zfill(size)
    return data, k


if __name__ == '__main__':
    k = 0

    sockC = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sockS = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    route_address = ('localhost', 8000)
    server_address = ('localhost', 10000)

    print('starting up on {} port {}'.format(*route_address))
    sockC.bind(route_address)

    sockC.listen(1)

    while True:
        print('waiting for a connection')
        connection, client_address = sockC.accept()

        print('connection from', client_address)

        print('connecting to {} port {}'.format(*server_address))
        sockS.connect(server_address)

        while True:
            data = sockS.recv(1000)
            if not data:
                print("No data")
                break
            else:
                #######
                d, k = eva(data, k)
                connection.sendall(d)
                #######

        connection.close()
        sockS.close()