import connection as CON
import diskUtils as DISK
import disHash as CHORD
import encode
import sys
import os
import time
import socket

#Index of files stored to the network
fileIndex = []

#This class defines the entries of the file index
class indexEntry():
    def __init__(self, fileName, keys):
        self.fileName = fileName
        self.keys = keys

def storeFile(fileName):
    #initializes a list of keys to be stored in the index
    keys = []
    #initializes a bytearray for storing the contents of the local file
    data = bytearray() 
    #Opens the file and stores it in data
    with open(fileName, 'rb') as file:
        byte = file.read(1)
        while byte:
           data.append(byte[0])
           byte = file.read(1)

    #adds checksum block to end of file
    data += encode.encode(data)
    #initializes a bytearray to store a blocks worth of data
    block = bytearray(DISK.blockSize)

    a = 0
    #breaks the data into blocks and sends them to the server to be stored
    while(a < len(data)):
        block = bytearray(DISK.blockSize)
        for i in range(DISK.blockSize):
            block[i] = data[a]
            a += 1
            if a >= len(data):
                break
        #creates a hash of the block to serve as a key to determine where it should be stored
        key = CHORD.hash(block)
        #connects to local server to start the process
        stub = CON.initializeClientConnection('127.0.0.1')
        #appends the key returned to the list of keys for the file index
        keys.append(stub.StoreBlock(CON.MESSAGE.StoreReq(key = key, data = bytes(block))).status)
    #appends the filename and list of keys to the file index
    fileIndex.append(indexEntry(fileName, keys))

def retrieveFile(fileName):
    #creates a data bucket for the data retrieved from the network
    data = bytearray()
    checksum = bytearray(DISK.blockSize)
    #searches the fileIndex for the filename
    for a in fileIndex:
        if a.fileName == fileName:
            #if the filename is found in the index, iterate over the keys in the index to retrieve each block of data
            for i in range(len(a.keys)):
                stub = CON.initializeClientConnection('127.0.0.1')
                if i == len(a.keys) - 1:
                    checksum = bytearray(stub.RetrieveBlock(CON.MESSAGE.RetrieveReq(key = i)).data)
                elif i != 2:
                    data += bytearray(stub.RetrieveBlock(CON.MESSAGE.RetrieveReq(key = i)).data)
    return encode.decode(data, checksum, 2)

def deleteFile(fileName):
    #iterates over all files in the index to find the filename
    for a in fileIndex:
        if a.fileName == fileName:
            #if the filename is found iterates over each block to unmute the nodes
            for i in a.keys:
                stub = CON.initializeClientConnection('127.0.0.1')
                stub.DeleteBlock(CON.MESSAGE.DeleteReq(key = i))

if __name__ == "__main__":
    #if no virtual disk is found, creates it
    if(not os.path.exists("disk.bin")):
        DISK.fdisk()
    #forks the client and server runtimes
    pid = os.fork()
    if(pid == 0):
        time.sleep(2)
        #discovers peers
        CON.createConnections()
        time.sleep(3)
        #if the user uses the store or load options determines the behaviour of the program
        if(len(sys.argv) > 1):
            if(sys.argv[1] == 'store'):
                if(socket.gethostname() == "client1"):
                    storeFile(sys.argv[2])
                    print(retrieveFile(sys.argv[2]).decode('utf-8'))
            if(sys.argv[1] == 'load'):
                retrieveFile(sys.argv[2])
    else:
        CON.initializeServerConnection()
