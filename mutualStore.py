import connection as CON
import diskUtils as DISK
import disHash as CHORD
import sys
import os
import time

def storeFile(data):
    block = bytearray(DISK.blockSize)
    a = 0
    while(a < len(data)):
        for i in range(DISK.blockSize):
            block[i] = data[a]
            a += 1
            if a >= len(data):
                break
        key = CHORD.hash(block)
        loc = CON.chord.inRange(key)
        if(loc > -1):
            DISK.saveBlock(loc, block)
        else:
            nextServer = CON.chord.mostPrev(key)
            stub = CON.initializeClientConnection(nextServer)
            stub.StoreBlock(CON.MESSAGE.StoreReq(key = key, data = block))

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
                with open(sys.argv[2], 'rb') as file:
                    data = bytearray()
                    byte = file.read(1)
                    while byte:
                        data.append(byte[0])
                        byte = file.read(1)
                    storeFile(data)
    else:
        CON.initializeServerConnection()
