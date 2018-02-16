# -*- coding: utf-8 -*-
import select
import socket

from my_socket import MySocket
from settings import BIND_ADDRESS, SERVER_PORT, MAX_CONNECTIONS, SELECT_TIMEOUT

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setblocking(0)
server_socket.bind((BIND_ADDRESS, SERVER_PORT))
server_socket.listen(MAX_CONNECTIONS)

potential_readers = [server_socket, ]
potential_writers = []
potential_errs = []
recv_messages = {}


def deal_client_socket(client_socket):
    my_socket = MySocket(client_socket)
    msg = my_socket.my_recv()
    my_socket.my_send(msg)
    my_socket.socket.close()


while True:
    ready_to_read, ready_to_write, in_error = \
        select.select(
            potential_readers,
            potential_writers,
            potential_errs,
            SELECT_TIMEOUT)

    for read_socket in ready_to_read:
        if read_socket is server_socket:
            client_socket, address = read_socket.accept()
            client_socket.setblocking(0)
            potential_readers.append(client_socket)
            potential_writers.append(client_socket)
        else:
            recv_messages[read_socket] = MySocket(read_socket).my_recv()

    for write_socket in ready_to_write:
        if write_socket in recv_messages:
            MySocket(write_socket).my_send(recv_messages[write_socket])
            # 流程结束，从监听列表中移除
            potential_readers.remove(write_socket)
            potential_writers.remove(write_socket)
