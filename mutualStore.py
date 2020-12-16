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
    a = 0
    #breaks the data into blocks and sends them to the server to be stored
    numBlocks = encode.round(float(len(data)) / float(DISK.blockSize))
    for n in range(numBlocks):
        block = bytearray(DISK.blockSize)
        for i in range(DISK.blockSize):
            a = n * DISK.blockSize + i
            if a < len(data):
                block[i] = data[a]
            else:
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
                #This causes block 4 to fail, to test the ability to recover
                if bc != 4:
                    blocks[bc] = bytearray(stub.RetrieveBlock(CON.MESSAGE.RetrieveReq(key = i),timeout = 10).data)
                    data += blocks[bc]
                else:
                    missingBlock = 4
                bc += 1
            time.sleep(.5)
        #if there is a missing block
        if missingBlock > -1:
            print("Recovering missing block number " + str(missingBlock))
            time.sleep(6)
            stub = CON.initializeClientConnection('127.0.0.1')
            #get the checksum from network storage
            checksum = bytearray(stub.RetrieveBlock(CON.MESSAGE.RetrieveReq(key = a.checkSumKey)).data)
            #decode the missing block using the other blocks and the checksum
            blocks[missingBlock] = encode.decode(data, checksum)
            #build the file with the missing block in the correct position
            data2 = bytearray()
            for a in blocks:
                data2 += a
            return data2
    #if no missing blocks return data, else return data2
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
    DISK.fdisk()
    #forks the client and server runtimes
    pid = os.fork()
    if(pid == 0):
        time.sleep(2)
        #discovers peers
        CON.createConnections()
        time.sleep(1)
        #if the user uses the store or load options determines the behaviour of the program
        if(len(sys.argv) > 1):
            if(sys.argv[1] == 'store'):
                #For testing client1 stores a file and then retrieves it
                if(socket.gethostname() == "client1"):
                    storeFile(sys.argv[2])
                    time.sleep(5)
                    print(retrieveFile(sys.argv[2]).decode('utf-8'))
            if(sys.argv[1] == 'load'):
                retrieveFile(sys.argv[2])
    else:
        #Start server
        CON.initializeServerConnection()
