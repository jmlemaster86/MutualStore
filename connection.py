import grpc
import rsa_pb2_grbc as REMOTE
import rsa_pb2 as MESSAGE
from concurrent import futures

class Server(REMOTE.SecureMessagingServicer):

    def storeBlock(self, request, context):

    def getBlock(self, request, context):

    def getInfo(self, request, context):

    def forwardRequest(self, request, context):


def initializeClientConnection(server_ip):
    channel = grpc.insecure_channel(server_ip + '50050')
    stub = REMOTE.SecureMessagingStub(channel)
    return stub

def initializeServerConnection():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    REMOTE.add_SecureMessagingServicer_to_server(Server(), server)
    server.add_insecure_port('[::]:50050')
    return server
