import diskUtils as DISK
import disHash as CHORD
import socket
import grpc
import os
import time
import mutualStore_pb2_grpc as REMOTE
import mutualStore_pb2 as MESSAGE
from concurrent import futures

#Server class to be passed to GRPC
class Server(REMOTE.SecureMessagingServicer):

    #initializes the distributed hash table
    def __init__(self):
        self.chord = CHORD.Nodes()

    def StoreBlock(self, request, context):
        #Checks if this system is responsible for the key
        testVal = self.chord.inRange(request.key)
        block = testVal[0]
        #If the node responsible is muted, the key is updated to successor of that node and the process is started over 
        if testVal[2]:
            stub = initializeClientConnection("127.0.0.1")
            return stub.StoreBlock(MESSAGE.StoreReq(key = testVal[1], data = request.data, name = request.name))
        #If the node responsible is not muted then store data to the block specified
        if block > -1:
            print("Storing data with key: " + str(request.key) + " in block: " + str(block))
            DISK.saveBlock(block, request.data)
            self.chord.mute(request.key)
            #Returns the key used in case it had to change it at some point due to muted nodes
            return MESSAGE.Confirmation(status = request.key)
        #If no virtual node on this system is responsible for the key, forward the request to the next server
        else:
            nextServer = self.chord.mostPrev(request.key)
            stub = initializeClientConnection(nextServer)
            print("Forwarding storage request with key: " + str(request.key) + " to " + str(nextServer))
            return stub.StoreBlock(MESSAGE.StoreReq(key = request.key, data = request.data, name = request.name))
        return MESSAGE.Confirmation(status = -1)

    def RetrieveBlock(self, request, context):
        #Checks if key is in range of any local virtual nodes
        block = self.chord.inRange(request.key)[0]
        if block > -1:
            #If the node responsible for the key is on this system, return the data stored in that nodes block
            print("Retrieving block")
            diskData = DISK.loadBlock(block)
            return MESSAGE.BlockMsg(data = diskData)
        else:
            #If the node responsible for the key is not on this system, forward the request to the next server.
            nextServer = self.chord.mostPrev(request.key)
            stub = initializeClientConnection(nextServer)
            print("Forwarding load request")
            return stub.RetrieveBlock(MESSAGE.RetrieveReq(request.key))
        return MESSAGE.BlockMsg(data = None)

    def DeleteBlock(self, request, context):
        #Checks if the key is in range of any local nodes
        block = self.chord.inRange(request.key)[0]
        if block > -1:
            #if a local node is responsible, unmute the node, which allows the block to be overwritten
            print("Deleting Block")
            self.chord.unmute(request.key)
            return MESSAGE.Confirmation(status = 1)
        else:
            #if no local node is responsible, forward the request to the next server.
            nextServer = self.chord.mostPrev(request.key)
            stub = initializeClientConnection(nextServer)
            print("Forwarding delete request")
            return stub.DeleteBlock(MESSAGE.DeleteReq(request.key))

    def JoinNode(self, request, context):
        #updates the finger tables of local nodes with the virtual nodes of the other client
        self.chord.update(request.ip, request.numBlocks)
        return MESSAGE.Confirmation(status = 1)


def initializeClientConnection(server_ip):
    #Creates a GRPC stub for client communication
    print("Initializing client connection to " + server_ip)
    channel = grpc.insecure_channel(server_ip + ':50050')
    stub = REMOTE.SecureMessagingStub(channel)
    return stub

def initializeServerConnection():
    #Creates GRPC server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=100))
    REMOTE.add_SecureMessagingServicer_to_server(Server(), server)
    server.add_insecure_port('[::]:50050')
    print("Starting server connection.")
    server.start()
    server.wait_for_termination()
    return server

def createConnections():
    #Creates all of the client connections for the docker compose testing
    for a in range(5):
        neighbor = ""
        name = 'client' + str(a+1)
        if(socket.gethostname() != name):
            neighbor = socket.gethostbyname(name)
            stub = initializeClientConnection(neighbor)
            stub.JoinNode(MESSAGE.JoinReq(ip = CHORD.ip, numBlocks = DISK.blockNum, name = ""))