import diskUtils
import hashlib
import socket

class Node():
    thisNode = ()
    fingers = []

    def createNode(self):
        ip = socket.gethostbyname(socket.gethostname())
        key = hash(ip)
        self.thisNode = (key, ip)
        return self

    def addFinger(self, ip):
        key = hash(ip)
        
        

class Table():
    entry = []

    def createTable(self):
        ip = socket.gethostbyname(socket.gethostname())
        for a in range(diskUtils.blockNum):
            key = hash(ip + ':' + str(a))
            node = Node()
            node.thisNode = (key, ip)
            self.entry.append(node)
        return self

    def addEntry(self, ip, block):
        for a in range(block):
            key = hash(ip + str(a))
            loc = self.find(key)
            if loc > -1:
                entry[loc].succesor = (key, ip)
        return self

    def find(self, key):
        for a in range(diskUtils.blockNum):
            try:
                if self.entry[a].thisNode[0] < key and self.entry[a + 1].thisNode[0] > key:
                    return a
            except:
                return -1

    


def hash(data):
    return int(hashlib.sha1(data).digest()[:10], 16)

if __name__ == "__main__":
    t = Table()
    t.createTable()
    t.addEntry('192.168.7.1', 10)

    for a in t.entry:
        print(a.thisNode)
        print(a.succesor)
