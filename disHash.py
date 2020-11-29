import diskUtils
import hashlib
import socket

numNodes = 8
ip = socket.gethostbyname(socket.gethostname())

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

    def mostPrev(self, k):
        result = (self.key, self.ip)
        for a in self.finger:
            if(a[1] == self.ip):
                continue
            oldDist = (k - result[0] + (2**numNodes)) % (2**numNodes)
            newDist = (k - a[0] + (2**numNodes)) % (2**numNodes)
            if(oldDist > newDist):
                result = a
            return result[1]
        return ""

    def inRange(self, k):
        if(self.prev[0] >= self.key):
            if(k <= self.key or k > self.prev[0]):
                return 1
        else:
            if(k <= self.key and k > self.prev[0]):
                return 1
        return 0
        


    def printFingers(self):
        for f in self.finger:
            print(f)

        

class Nodes:

    def __init__(self):
        self.nodes = []
        for a in range(diskUtils.blockNum):
            self.addNode(hash((ip + str(a)).encode("utf-8")), ip)


    def addNode(self, k, i):
        self.nodes.append(Node(k,i))
        for a in range(len(self.nodes)):
            self.nodes[len(self.nodes) - 1].addPrev(self.nodes[a].key, self.nodes[a].ip)
            self.nodes[len(self.nodes) - 1].addFinger(self.nodes[a].key, self.nodes[a].ip)
        for a in range(len(self.nodes)):
            self.nodes[a].addPrev(k,i)
            self.nodes[a].addFinger(k,i)

    def update(self, i, numBlocks):
        for p in range(numBlocks):
            k = hash((i + str(p)).encode("utf-8"))
            for a in range(len(self.nodes)):
                self.nodes[a].addPrev(k, i)
                self.nodes[a].addFinger(k, i)

    def mostPrev(self, k):
        result = self.nodes[0]
        for a in self.nodes:
            oldDist = (k - result.key + (2**numNodes)) % (2**numNodes)
            newDist = (k - a.key + (2**numNodes)) % (2**numNodes)
            if(oldDist > newDist):
                result = a
        return result.mostPrev(k)

    def inRange(self, k):
        for a in range(diskUtils.blockNum):
            if self.nodes[a].inRange(k) > 0:
                return a
        return -1
            


def hash(data):
    return int(hashlib.sha1(data).hexdigest()[:10], 16) % 2**numNodes


if __name__ == "__main__":
    N = Nodes()
    for node in N.nodes:
        node.printFingers()
