import diskUtils
import hashlib
import socket

power = 10
numNodes = 2**power
ip = socket.gethostbyname(socket.gethostname())

class Node():

    def __init__(self, k, i):
        self.key = k
        self.ip = i
        self.finger = []
        self.muted = False
        self.prev = (k, i)
        for a in range(numNodes):
            self.finger.append((self.key, self.ip))

    def addPrev(self, k, i):
        oldDist = (self.key - self.prev[0]  + (numNodes - 1)) % (numNodes)
        newDist = (self.key - k + (numNodes - 1)) % (numNodes)
        if(oldDist > newDist):
            self.prev = (k, i)

    def addFinger(self, k, i):
        for a in range(numNodes):
            testKey = (self.key + 2**a) % (numNodes)
            oldDist = (self.finger[a][0] - testKey + (numNodes)) % (numNodes)
            newDist = (k - testKey + (numNodes)) % (numNodes)
            if(oldDist > newDist):
                self.finger[a] = (k,i)

    def mostPrev(self, k):
        result = (self.key, self.ip)
        for a in self.finger:
            oldDist = (k - result[0] + (numNodes)) % (numNodes)
            newDist = (k - a[0] + (numNodes)) % (numNodes)
            if(oldDist > newDist):
                result = a
        print("The most prev of " + str(k) + " is " + str(result))
        return result

    def inRange(self, k):
        print("Checking if " + str(k) + " is in range " + str(self.prev[0]) + " - " + str(self.key))
        if(self.prev[0] >= self.key):
            if(k <= self.key or k > self.prev[0]):
                return 1
        else:
            if(k <= self.key and k > self.prev[0]):
                return 1
        return 0

    def directSuccessor(self):
        return self.finger[0]
        


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
        result = self.nodes[0].mostPrev(k)
        for a in self.nodes:
            oldDist = (k - result[0] + (numNodes)) % (numNodes)
            newDist = (k - a.mostPrev(k)[0] + (numNodes)) % (numNodes)
            if(oldDist > newDist):
                result = a.mostPrev(k)
        if(result[1] == ip):
            for a in self.nodes:
                if a.key == result[0]:
                    result = a.directSuccessor()
        return result[1]

    def inRange(self, k):
        b = 0
        while b < diskUtils.blockNum:
            if(self.nodes[b].inRange(k) > 0):
                return(b, self.nodes[b].directSuccessor()[0], self.nodes[b].muted)
            b += 1
        return(-1, -1, False)

    def mute(self, k):
        b = 0
        while b < diskUtils.blockNum:
            if(self.nodes[b].inRange(k) > 0):
                self.nodes[b].muted = True
            b += 1





def hash(data):
    return int(hashlib.sha1(data).hexdigest()[:10], 16) % numNodes


if __name__ == "__main__":
    N = Nodes()
    for node in N.nodes:
        node.printFingers()
