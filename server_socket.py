# -*- coding: utf-8 -*-
import socket

BIND_ADDRESS = '0.0.0.0'
SERVER_PORT = 8888
MAX_CONNECTIONS = 5

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((BIND_ADDRESS, SERVER_PORT))
server_socket.listen(MAX_CONNECTIONS)


def client_thread(client_socket):
    pass


while True:
    client_socket, address = server_socket.accept()
    client_thread(client_socket)
    client_socket.run()