# -*- coding: utf-8 -*-
import socket

from my_socket import MySocket
from settings import BIND_ADDRESS, SERVER_PORT

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((BIND_ADDRESS, SERVER_PORT))
msg = input('请输入要发送的信息：')
my_socket = MySocket(client_socket)
my_socket.my_send(msg)
reply = my_socket.my_recv()
print('接收到的信息：{}'.format(reply))
