import socket
import sys
import time


if __name__ == '__main__':
    L = 40

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 10000)
    print('starting up on {} port {}'.format(*server_address))
    sock.bind(server_address)

    sock.listen(1)

    while True:
        print('waiting for a connection')
        connection, client_address = sock.accept()
        try:
            print('connection from', client_address)
            while True:
                data = b'This is the message.'
                if len(data) < L:
                    connection.sendall(data)
                    print('send', data)
                else:
                    for item in [data[i:i + L] for i in range(0, len(data), L)]:
                        connection.sendall(item)
                        print('send', item)
                time.sleep(10.0)

        finally:
            connection.close()