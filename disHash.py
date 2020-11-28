import diskUtils
import hashlib
import socket

numNodes = 8

class Node():

    def __init__(self, k, i):
        self.key = k
        self.ip = i
        self.finger = []
        self.prev = (k, i)
        for a in range(numNodes):
            self.finger.append((self.key, self.ip))

    def addPrev(self, k, i):
        oldDist = (self.key - self.prev[0]  + (2**numNodes - 1)) % (2**numNodes)
        newDist = (self.key - k + (2**numNodes - 1)) % (2**numNodes)
        if(oldDist > newDist):
            self.prev = (k, i)

    def addFinger(self, k, i):
        for a in range(numNodes):
            testKey = (self.key + 2**a) % (2**numNodes)
            oldDist = (self.finger[a][0] - testKey + (2**numNodes)) % (2**numNodes)
            newDist = (k - testKey + (2**numNodes)) % (2**numNodes)
            if(oldDist > newDist):
                self.finger[a] = (k,i)

    def printFingers(self):
        for f in self.finger:
            print(f)

class Nodes:

    def __init__(self):
        self.nodes = []

    def addNode(self, k, i):
        self.nodes.append(Node(k,i))
        for a in range(len(self.nodes)):
            self.nodes[len(self.nodes) - 1].addPrev(self.nodes[a].key, self.nodes[a].ip)
            self.nodes[len(self.nodes) - 1].addFinger(self.nodes[a].key, self.nodes[a].ip)
        for a in range(len(self.nodes)):
            self.nodes[a].addPrev(k,i)
            self.nodes[a].addFinger(k,i)

    def update(self, k, i):
        for a in range(len(self.nodes)):
            self.nodes[a].addPrev(k, i)
            self.nodes[a].addFinger(k, i)

def hash(data):
    return int(hashlib.sha1(data).hexdigest()[:10], 16) % 2**numNodes

if __name__ == "__main__":
    ip = socket.gethostbyname(socket.gethostname())
    N = Nodes()
    for a in range(diskUtils.blockNum):
        key = hash(ip + str(a))
        N.addNode(key,ip)

    for node in N.nodes:
        node.printFingers()