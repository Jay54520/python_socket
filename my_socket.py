# -*- coding: utf-8 -*-
import socket

from settings import BUFFER_MAXSIZE, MSGLEN, COMPLEMENT_CHAR


class MySocket:

    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

    def my_send(self, msg: str):
        msg = self.complete_msg(msg)
        msg = msg.encode('utf-8')
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
        return self.parse_msg(b''.join(chunks).decode())

    def complete_msg(self, msg):
        if len(msg) != MSGLEN:
            return msg + COMPLEMENT_CHAR * (MSGLEN - len(msg))
        return msg

    def parse_msg(self, msg):
        if msg.endswith(COMPLEMENT_CHAR):
            return msg.strip(COMPLEMENT_CHAR)
        return msg
