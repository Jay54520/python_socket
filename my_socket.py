# -*- coding: utf-8 -*-
import socket

BUFFER_MAXSIZE = 2048
MSGLEN = 4096


class MySocket:

    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

    def my_send(self, msg):
        total_sent = 0
        while total_sent != MSGLEN:
            sent = self.sock.send(msg[total_sent:])
            if sent == 0:
                raise RuntimeError('连接已关闭')
            total_sent += sent

    def my_recv(self):
        total_recv = 0
        chunks = []
        while total_recv != MSGLEN:
            chunk = self.sock.recv(min(MSGLEN - total_recv, BUFFER_MAXSIZE))
            if chunk == b'':
                raise RuntimeError('连接已关闭')
            total_recv += len(chunk)
            chunks.append(chunk)
        return b''.join(chunks)