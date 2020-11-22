import diskUtils
import hashlib
import socket

class fingerTable():
    entry = []

    def createTable(self):
        ip = socket.gethostbyname(socket.gethostname())
        for a in range(diskUtils.blockNum):
            key = hash(ip + ':' + str(a))
            self.entry.append((key, ip))
        return self

    def addEntry(self, ip, block):
        key = hash(ip + ':' + str(block))
        self.entry.append((key, ip))
        return self


def hash(data):
    return hashlib.sha1(data)

if __name__ == "__main__":
    f = fingerTable()
    f.createTable()
    for a in f.entry:
        print(str(a))
