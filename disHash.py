import diskUtils
import hashlib
import socket

#power determines the number of finger tables each node has
power = 10
#numNodes is used for the mod functions in determining distance in the distributed hash table
numNodes = 2**power

#this systems ip address
ip = socket.gethostbyname(socket.gethostname())

#Objects of this class are individual virtual nodes in a distributed hash table
class Node():

    def __init__(self, k, i):
        #Initializes the key, ip,  muted status, previous node, and finger table for this node
        self.key = k
        self.ip = i
        self.finger = []
        self.muted = False
        self.prev = (k, i)
        for a in range(power):
            self.finger.append((self.key, self.ip))

    def addPrev(self, k, i):
        #takes a key and ip pair and checks if it is a better candidate to be a previous node
        oldDist = (self.key - self.prev[0]  + (numNodes - 1)) % (numNodes) #distance on the circle between current prev and this node
        newDist = (self.key - k + (numNodes - 1)) % (numNodes) #distance on the circle between candidate node and this node
        if(oldDist > newDist): #if candidate node is closer it becomes the new prev
            self.prev = (k, i)

    def addFinger(self, k, i):
        # iterates across the finger table
        for a in range(power):
            testKey = (self.key + 2**a) % (numNodes) #test key is the floor of what the ath finger should cover
            oldDist = (self.finger[a][0] - testKey + (numNodes)) % (numNodes) #distance between current entry and floor
            newDist = (k - testKey + (numNodes)) % (numNodes) #distance between candidate entry and floor
            if(oldDist > newDist): #if the candidate entry is closer to the floor value it becomes the new entry
                self.finger[a] = (k,i)

    def mostPrev(self, k):
        #searches finger table for the node that is closest to k without going over
        result = (self.key, self.ip) #initialize result as self
        for a in self.finger: #check each finger
            oldDist = (k - result[0] + (numNodes)) % (numNodes) #distance between test value k and current result
            newDist = (k - a[0] + (numNodes)) % (numNodes) #distance between test value k and finger a
            if(oldDist > newDist): #if finger a is closer to k without going over it becomes the new result
                result = a
        return result

    def inRange(self, k):
        #checks if this node is responsible for key k
        if(self.prev[0] >= self.key): #checks the case where 0 lies between this node and prev
            if(k <= self.key or k > self.prev[0]):
                return 1
        else:
            if(k <= self.key and k > self.prev[0]):
                return 1
        #returns 1 if k false between prev and self, returns 0 otherwise
        return 0

    def directSuccessor(self):
        #returns the direct successor of this node
        return self.finger[0]

    def printFingers(self):
        #for testing purpose, prints the finger table of this node
        for f in self.finger:
            print(f)

        
#This class is the collection of virtual nodes on this system
class Nodes:

    def __init__(self):
        #initialize an array of virtual nodes
        self.nodes = []
        for a in range(diskUtils.blockNum):
            #uses ip address + block number to create hash key and creates a new virtual node
            self.addNode(hash((ip + str(a)).encode("utf-8")), ip)


    def addNode(self, k, i):
        #adds local nodes to the collection of nodes
        self.nodes.append(Node(k,i))
        #updates the finger table of this new node with the previous nodes
        for a in range(len(self.nodes)):
            self.nodes[len(self.nodes) - 1].addPrev(self.nodes[a].key, self.nodes[a].ip)
            self.nodes[len(self.nodes) - 1].addFinger(self.nodes[a].key, self.nodes[a].ip)
        #updates the existing nodes' finger tables
        for a in range(len(self.nodes)):
            self.nodes[a].addPrev(k,i)
            self.nodes[a].addFinger(k,i)

    def update(self, i, numBlocks):
        #updates the finger tables of every virtual node to include the virtual nodes of another client
        for p in range(numBlocks):
            k = hash((i + str(p)).encode("utf-8"))
            for a in range(len(self.nodes)):
                self.nodes[a].addPrev(k, i)
                self.nodes[a].addFinger(k, i)

    def mostPrev(self, k):
        #Calls the mostPrev of each node and finds the over all most previous node
        result = self.nodes[0].mostPrev(k)
        for a in self.nodes:
            oldDist = (k - result[0] + (numNodes)) % (numNodes)
            newDist = (k - a.mostPrev(k)[0] + (numNodes)) % (numNodes)
            if(oldDist > newDist):
                result = a.mostPrev(k)
        #If the most previous node to k is a local virtual node we return the direct successor of that virtual node
        if(result[1] == ip):
            for a in self.nodes:
                if a.key == result[0]:
                    result = a.directSuccessor()
        return result[1]

    def inRange(self, k):
        #Checks if any virtual node on this system is responsible for key k
        for b in range(diskUtils.blockNum):
            if(self.nodes[b].inRange(k) > 0):
                #if virtual node b is responsible for k return a tuple of the block number b, the direct successor of node b, and whether or not node b is muted
                return(b, self.nodes[b].directSuccessor()[0], self.nodes[b].muted)
        return(-1, -1, False)

    def mute(self, k):
        #mutes the node responsible for key k, muted nodes cannot be used for storage but their finger tables are still available for use
        for b in range(diskUtils.blockNum):
            if(self.nodes[b].inRange(k) > 0):
                self.nodes[b].muted = True
            b += 1

    def unmute(self, k):
        #unmutes the node responsible for key k, used when deleting a file
        for b in range(diskUtils.blockNum):
            if(self.nodes[b].inRange(k) > 0):
                self.nodes[b].muted = False

def hash(data):
    #creates a int hash of the data mod the number of nodes posible
    return int(hashlib.sha1(data).hexdigest()[:10], 16) % numNodes
