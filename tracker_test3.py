# -*- coding: utf-8 -*-
__author__ = 'liubei'
import triad_openvr
import time
import sys
import struct
import socket
import thread
import os
import hashlib

HOST = '192.168.192.100'
PORT = 7777

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(5)

print 'Server start at: %s:%s' % (HOST, PORT)
print 'wait for connection...'

conn, addr = s.accept()
print 'Connected by ', addr

# v = triad_openvr.triad_openvr()
# v.print_discovered_objects()

if len(sys.argv) == 1:
    interval = 1.0 / 20
elif len(sys.argv) == 2:
    interval = 1 / float(sys.argv[0])
else:
    print("Invalid number of arguments")
    interval = False

print "interval : %.2f" % interval

s.close()


def send_mock(conn, s, txt, type):
    # ss = txt.split(" ")
    if "VR" == txt[0]:
        tmpStr = [int(txt[2]), float(txt[3]) * 1, 0 * float(txt[4]), float(txt[5]), float(txt[6]), float(txt[7]),
                  float(txt[8]), 0]
    else:
        tmpStr = [int(txt[2]), float(txt[3]), float(txt[4]), float(txt[5]), float(txt[6]), float(txt[7]), float(txt[8]),
                  0]

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

def sendStr(conn, s, txt, type):
    tmpStr = txt
    print tmpStr

    header = [type, tmpStr.__len__(), 0, 0]

    headPack = struct.pack("@4I", *header)

    bodyPack = struct.pack("@9s", *tmpStr)
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

def send(conn, s, txt, type):
    tmpStr = [int(0), float(txt[0]), float(txt[1]), float(txt[2]), float(0.0), float(0.0), float(0.0), 0]
    # tmpStr = [int(txt[2]), float(txt[3]) * 1, 0 * float(txt[4]), float(txt[5]), float(txt[6]), float(txt[7]),
    #           float(txt[8]), 0]
    print tmpStr

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


def vr_body_slam_mock_server(f):
    with open(f) as ff:
        contents = [x.strip() for x in ff.readlines()]
        for content in contents:
            strs = content.split(" ")
            if len(strs) < 9:
                continue
            if strs[0] == 'VR':
                send_mock(conn, s, strs, 3)
            elif strs[0] == 'Slam':
                send_mock(conn, s, strs, 4)
            elif strs[0] == 'Robot':
                send_mock(conn, s, strs, 0)
            time.sleep(1.0 / 100)

def cam_server(f):
    done = False
    while(True):
        print "cam server alive"
        if not os.path.exists(f):
            print "%s file not exist " % f
            send(conn, s, "-100 -100 -100", 5)
            time.sleep(1)
        #if done:
        #    print "file has read done"
        #    continue
        try:
            with open(f) as ff:
                #done = True

                contents = [x.strip() for x in ff.readlines()]
                for content in contents:
                    strs = content.split(" ")
                    print "<<<<< reading file <<<<<<"
                    send(conn, s, strs, 5)
                    time.sleep(1.0 / 10)
                #send camera end
                send(conn, s, "-100 -100 -100", 5)
                time.sleep(1)
        except Exception,e:
            print(e)
            
def vr_server(conn, s):
    v = triad_openvr.triad_openvr()
    v.print_discovered_objects()

    index = 0
    while (True):
        start = time.time()
        txt = ""
        for each in v.devices["tracker_1"].get_pose_euler():
            txt += "%.4f" % each
            txt += " "

        ss = txt.split(" ")
        tmpStr = [start, -1 * float(ss[0]), float(ss[1]), float(ss[2]), float(ss[3]), float(ss[4]), float(ss[5]), 0]

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


try:
    #thread.start_new_thread(vr_server, (conn, s))
    thread.start_new_thread(cam_server, ("cam/cam_path.txt",))
    thread.start_new_thread(vr_body_slam_mock_server, ("bakupup/comm_client_log_07_08_04.txt",))
except Exception, e:
    print(e)
    print "Error: unable to start thread"

while 1:
    pass
