# -*- coding: utf-8 -*-
__author__ = 'liubei'
import triad_openvr
import time
import sys
import struct
import socket

HOST = '192.168.1.115'
PORT = 7777

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(5)

print 'Server start at: %s:%s' % (HOST, PORT)
print 'wait for connection...'

v = triad_openvr.triad_openvr()
v.print_discovered_objects()

if len(sys.argv) == 1:
    interval = 1.0 / 10
elif len(sys.argv) == 2:
    interval = 1 / float(sys.argv[0])
else:
    print("Invalid number of arguments")
    interval = False

print "interval : %.2f" % interval

conn, addr = s.accept()
print 'Connected by ', addr

index = 0
while (True):
    start = time.time()
    txt = ""
    for each in v.devices["controller_1"].get_pose_euler():
        txt += "%.4f" % each
        txt += " "

    # tmpStr = "\r" + str(index) + " " + str(start) + " " + txt
    # tmpStr = [start, 1.1759, 0.7149, -0.1582, -28.4829, -84.2658, 41.7791, 0]
    ss = txt.split(" ")
    tmpStr = [start, float(ss[0]), float(ss[1]), float(ss[2]), float(ss[3]), float(ss[4]), float(ss[5]), 0]

    print(tmpStr)

    header = [3, tmpStr.__len__(), 0, 0]
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

    index += 1

    sleep_time = interval - (time.time() - start)
    if sleep_time > 0:
        time.sleep(sleep_time)

s.close()
