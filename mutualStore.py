import connection as CON
import diskUtils as DISK
import disHash as CHORD
import sys
import os
import time
import socket

def storeFile(fileName):
    data = bytearray()
    with open(fileName, 'rb') as file:
        byte = file.read(1)
        while byte:
           data.append(byte[0])
           byte = file.read(1)
    block = bytearray(DISK.blockSize)
    a = 0
    while(a < len(data)):
        for i in range(DISK.blockSize):
            block[i] = data[a]
            a += 1
            if a >= len(data):
                break
        key = CHORD.hash(block)
        CON.initializeClientConnection('127.0.0.1')

def retrieveFile(name):
    return None

if __name__ == "__main__":
    if(not os.path.exists("disk.bin")):
        DISK.fdisk()
    pid = os.fork()
    if(pid == 0):
        time.sleep(2)
        if(len(sys.argv) > 1):
            if(sys.argv[1] == 'store'):
                storeFile(sys.argv[2])
    else:
        CON.initializeServerConnection()
