import triad_openvr
import time
import sys

import socket

HOST = '192.168.1.61'
PORT = 8001

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(5)

print 'Server start at: %s:%s' % (HOST, PORT)
print 'wait for connection...'

v = triad_openvr.triad_openvr()
v.print_discovered_objects()

if len(sys.argv) == 1:
    interval = 1 / 250
elif len(sys.argv) == 2:
    interval = 1 / float(sys.argv[0])
else:
    print("Invalid number of arguments")
    interval = False

conn, addr = s.accept()
print 'Connected by ', addr

while (True):
    start = time.time()
    txt = ''
    for each in v.devices["controller_1"].get_pose_euler():
        txt += "%.4f" % each
        txt += " "

    tmpStr = "\r" + str(start) + " " + txt
    print(tmpStr)

    conn.send(tmpStr)

    sleep_time = interval - (time.time() - start)
    if sleep_time > 0:
        time.sleep(sleep_time)