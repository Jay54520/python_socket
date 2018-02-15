# -*- coding: utf-8 -*-
import socket

from settings import BUFFER_MAXSIZE, MSG_PREFIX_LENGTH


class MySocket:

    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

    def my_send(self, msg: bytes):
        msg = self.complete_msg(msg)
        msg_length = len(msg)
        total_sent = 0
        while total_sent != msg_length:
            sent = self.sock.send(msg[total_sent:])
            if sent == 0:
                raise RuntimeError('连接已关闭')
            total_sent += sent

    def my_recv(self) -> bytes:
        # 获取信息体长度
        body_length = int(self._recv(MSG_PREFIX_LENGTH).decode())
        return self._recv(body_length)

    def complete_msg(self, msg):
        """给消息加上 5 位的消息长度前缀"""
        bytes_body_length = str(len(msg)).encode()
        bytes_body_length = b'0' * (MSG_PREFIX_LENGTH - len(bytes_body_length)) + bytes_body_length
        msg = bytes_body_length + msg
        return msg

    def _recv(self, msg_length) -> bytes:
        """
        获取 msg_length 长度的信息
        :param msg_length: 要获取的信息的长度
        :return:
        """
        total_recv = 0
        chunks = []
        while total_recv != msg_length:
            chunk = self.sock.recv(min(msg_length - total_recv, BUFFER_MAXSIZE))
            if chunk == b'':
                raise RuntimeError('连接已关闭')
            total_recv += len(chunk)
            chunks.append(chunk)
        return b''.join(chunks)

    @property
    def socket(self):
        return self.sock