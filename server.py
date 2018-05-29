import socket
import argparse
from utils import *

parser = argparse.ArgumentParser(description='Simple Cached Server')
parser.add_argument('-H', '--host', default='127.0.0.1')
parser.add_argument('-p', '--port', default='8000')
args = parser.parse_args()

SERVER_HOST = str(args.host)
SERVER_PORT = int(args.port)

server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(1)

print("Listening on %s:%d..." % (SERVER_HOST, SERVER_PORT))
try:
    while True:
        client_conn, client_addr = server_socket.accept()
        req = client_conn.recv(1024).decode()
        headers = resolve_req(req)
        print('{0}:{1}->{2}'.format(client_addr[0], client_addr[1], headers['REQ']))
        try:
            res = 'HTTP/1.0 200 OK\n\n' + route(headers['REQ'])
            client_conn.sendall(res.encode())
        except FileNotFoundError:
            client_conn.sendall('HTTP/1.0 404 Not Found\n\nNot Found'.encode())
        client_conn.close()
except KeyboardInterrupt:
    print("\rExited!", end=' ')

finally:
    server_socket.close()
