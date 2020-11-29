import diskUtils as DISK
import disHash as CHORD
import socket
import grpc
import os
import time
import mutualStore_pb2_grpc as REMOTE
import mutualStore_pb2 as MESSAGE
from concurrent import futures


class Server(REMOTE.SecureMessagingServicer):

    def __init__(self):
        self.chord = CHORD.Nodes()

    def StoreBlock(self, request, context):
        block = self.chord.inRange(request.key)
        if block > -1:
            print("Storing data")
            DISK.saveBlock(block, request.data)
            return MESSAGE.Confirmation(status = 1)
        else:
            nextServer = self.chord.mostPrev(request.key)
            stub = initializeClientConnection(nextServer)
            print("Forwarding storage request.")
            return stub.StoreBlock(MESSAGE.StoreReq(key = request.key, data = request.data))
        return MESSAGE.Confirmation(status = 0)

    def RetrieveBlock(self, request, context):
        block = self.chord.inRange(request.key)
        if block > -1:
            print("Retrieving block")
            diskData = DISK.loadBlock(block)
            return MESSAGE.BlockMsg(data = diskData)
        else:
            nextServer = self.chord.mostPrev(request.key)
            stub = initializeClientConnection(nextServer)
            print("Forwarding load request")
            return stub.RetrieveBlock(MESSAGE.RetrieveReq(request.key))
        return MESSAGE.BlockMsg(data = None)

    def JoinNode(self, request, context):
        result = 0
        try:
            self.chord.update(request.ip, request.numBlocks)
            result = 1
        except:
            print("Unable to update.")
        return MESSAGE.Confirmation(status = result)


def initializeClientConnection(server_ip):
    print("Initializing client connection to " + server_ip)
    channel = grpc.insecure_channel(server_ip + ':50050')
    stub = REMOTE.SecureMessagingStub(channel)
    return stub

def initializeServerConnection():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    REMOTE.add_SecureMessagingServicer_to_server(Server(), server)
    server.add_insecure_port('[::]:50050')
    print("Starting server connection.")
    server.start()
    server.wait_for_termination()
    return server

def createConnections():
    neighbor = ""
    if socket.gethostname() == "client1":
        neighbor = socket.gethostbyname("client2")
    else:
        neighbor = socket.gethostbyname("client1")
    stub = initializeClientConnection(neighbor)
    stub.JoinNode(MESSAGE.JoinReq(ip = CHORD.ip, numBlocks = DISK.blockNum))

if __name__ == "__main__":
    pid = os.fork()
    if pid == 0:
        time.sleep(4)
        neighbor = ""
        if(socket.gethostname() == "client1"):
            neighbor = socket.gethostbyname("client2")
        else:
            neighbor = socket.gethostbyname("client1")
        stub = initializeClientConnection(neighbor)
        stub.JoinNode(MESSAGE.JoinReq(ip = CHORD.ip, numBlocks = DISK.blockNum))
        if neighbor == socket.gethostbyname("client2"):
            for a in range(10):
                stub.StoreBlock(MESSAGE.StoreReq(key = a, data = bytes("Hello World", 'utf-8')))
    else:
        initializeServerConnection()
