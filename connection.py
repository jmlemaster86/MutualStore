import diskUtils as DISK
import disHash as CHORD
import grpc
import mutualStore_pb2_grbc as REMOTE
import mutualStore_pb2 as MESSAGE
from concurrent import futures


class Server(REMOTE.SecureMessagingServicer):
    
    def __init__(self):
        self.chord = CHORD.Nodes()

    def storeBlock(self, request, context):
        return None

    def getBlock(self, request, context):
        return None

    def joinNode(self, request, context):
        result = 0
        try:
            self.chord.update(request.ip, request.numBlocks)
            result = 1
        except:
            print("Unable to update.")
        return MESSAGE.Confirmation(status = result)


def initializeClientConnection(server_ip):
    channel = grpc.insecure_channel(server_ip + '50050')
    stub = REMOTE.SecureMessagingStub(channel)
    return stub

def initializeServerConnection():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    REMOTE.add_SecureMessagingServicer_to_server(Server(), server)
    server.add_insecure_port('[::]:50050')
    return server