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
    def __init__(self, fileName, keys, checkSumKey):
        self.fileName = fileName
        self.keys = keys
        self.checkSumKey = checkSumKey

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
    #initializes a bytearray to store a blocks worth of data
    block = bytearray(DISK.blockSize)
    a = 0
    #breaks the data into blocks and sends them to the server to be stored
    while(a < len(data)):
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
    #Creates checksum block and stores it on the network
    checksum = encode.encode(data)
    key = CHORD.hash(checksum)
    stub = CON.initializeClientConnection('127.0.0.1')
    checkSumKey = stub.StoreBlock(CON.MESSAGE.StoreReq(key = key, data = bytes(checksum))).status
    #adds filename and list of keys to file index
    fileIndex.append(indexEntry(fileName, keys, checkSumKey))

def retrieveFile(fileName):
    #creates a data bucket for the data retrieved from the network
    data = bytearray()
    checksum = bytearray(DISK.blockSize)
    missingBlock = -1
    #searches the fileIndex for the filename
    for a in fileIndex:
        if a.fileName == fileName:
            bc = 0
            blocks = [bytearray(DISK.blockSize)] * len(a.keys)
            #if the filename is found in the index, iterate over the keys in the index to retrieve each block of data
            for i in a.keys:
                stub = CON.initializeClientConnection('127.0.0.1')
                blocks[bc] = bytearray(stub.RetrieveBlock(CON.MESSAGE.RetrieveReq(key = i)).data)
                data += blocks[bc]
                bc += 1
        if missingBlock > -1:
            print("Recovering missing block number " + str(missingBlock))
            stub = CON.initializeClientConnection('127.0.0.1')
            checksum = bytearray(stub.RetrieveBlock(CON.MESSAGE.RetrieveReq(key = a.checkSumKey)).data)
            time.sleep(2)
            blocks[missingBlock] = encode.decode(data, checksum)
            data2 = bytearray()
            for a in blocks:
                data2 += a
            return data2
    return data

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
