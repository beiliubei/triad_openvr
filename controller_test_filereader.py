# -*- coding: utf-8 -*-
__author__ = 'liubei'
import time
import sys
import struct
import socket

HOST = '192.168.1.55'
# PORT = 7777
PORT = int(sys.argv[3])

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(5)

print 'Server start at: %s:%s' % (HOST, PORT)
print 'wait for connection...'

conn, addr = s.accept()
print 'Connected by ', addr

# index = 0

def send(conn, s, txt, type):
    #ss = txt.split(" ")
    if txt[0] == 'VR':
        tmpStr = [int(txt[2]), float(txt[3]) * 1, 0, float(txt[5]), float(txt[6]), float(txt[7]), float(txt[8]), 0]
    else:
        tmpStr = [int(txt[2]), float(txt[3]), float(txt[4]), float(txt[5]), float(txt[6]), float(txt[7]), float(txt[8]), 0]

    print(tmpStr)

    header = [type, tmpStr.__len__(), 0, 0]
    headPack = struct.pack("@4I", *header)

    bodyPack = struct.pack("@I6fI", *tmpStr)
    # headPack = str(tmpStr.__len__()).zfill(12)
    sendData = headPack + bodyPack
    try:
        conn.send(sendData)
    except Exception:
        s.close()
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((HOST, PORT))
        s.listen(5)

        print 'Server start at: %s:%s' % (HOST, PORT)
        print 'wait for connection...'

        conn, addr = s.accept()
        print 'Connected by ', addr

    # index += 1

while (True):
    f = sys.argv[1]
    type = sys.argv[2]
    with open(f) as ff:
        contents = [x.strip() for x in ff.readlines()]
        for content in contents:
            strs = content.split(" ")
            if len(strs) < 9:
                continue
            if strs[0] == 'VR' and type == "3":
                send(conn, s, strs, 3)
            elif strs[0] == 'Robot' and type == "0":
                pass
                send(conn, s, strs, 0)
            time.sleep(1.0/20)

    # tmpStr = "\r" + str(index) + " " + str(start) + " " + txt
    # tmpStr = [start, 1.1759, 0.7149, -0.1582, -28.4829, -84.2658, 41.7791, 0]


s.close()
