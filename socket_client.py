# -*- coding: utf-8 -*-
__author__ = 'liubei'
import socket
from time import sleep
import struct

HOST = '192.168.1.121'
PORT = 8001

dataBuffer = bytes()
headerSize = 12

sn = 0


def dataHandle(body):
    global sn
    sn += 1
    # print("第%s个数据包" % sn)
    # print("ver:%s, bodySize:%s, cmd:%s" % headPack)
    print(body.decode())
    # print("")


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

while True:
    # cmd = raw_input("Please input msg:")
    # s.send(cmd)
    data = s.recv(4096)
    # print data.decode()
    if data:
        dataBuffer += data
        while True:
            if len(dataBuffer) < headerSize:
                # print("数据包（%s Byte）小于包头长度，跳出小循环" % len(dataBuffer))
                break

            # 读取包头
            # struct中:!代表Network order，3I代表3个unsigned int数据
            # headPack = struct.unpack('!3I', dataBuffer[:headerSize])
            # bodySize = headPack[1]

            bodySize = dataBuffer[:headerSize]

            # 分包情况处理，跳出函数继续接收数据
            if len(dataBuffer) < headerSize + bodySize:
                # print("数据包（%s Byte）不完整（总共%s Byte），跳出小循环" % (len(dataBuffer), headerSize + bodySize))
                break
            # 读取包体的内容
            body = dataBuffer[headerSize:headerSize + bodySize]

            dataHandle(body)

            # 粘包情况的处理
            dataBuffer = dataBuffer[headerSize + bodySize:]
