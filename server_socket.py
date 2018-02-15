# -*- coding: utf-8 -*-
import socket
import threading

from my_socket import MySocket
from settings import BIND_ADDRESS, SERVER_PORT, MAX_CONNECTIONS

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((BIND_ADDRESS, SERVER_PORT))
server_socket.listen(MAX_CONNECTIONS)


def deal_client_socket(client_socket):
    my_socket = MySocket(client_socket)
    msg = my_socket.my_recv()
    my_socket.my_send(msg)


def client_thread(client_socket):
    return threading.Thread(target=deal_client_socket, args=(client_socket, ))


while True:
    client_socket, address = server_socket.accept()
    ct = client_thread(client_socket)
    try:
        ct.run()
    except RuntimeError as e:
        print(e)
