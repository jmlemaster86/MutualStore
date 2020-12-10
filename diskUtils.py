blockSize = 256
blockNum = 2
diskSize = blockSize * blockNum
    
def fdisk():
    with open('disk.bin', 'wb') as disk:
        disk.write(bytearray(diskSize))

def saveBlock(loc, data):
    with open('disk.bin', 'r+b') as disk:
        disk.seek(loc * blockSize)
        disk.write(data)
        
def loadBlock(loc):
    with open('disk.bin', 'rb') as disk:
        disk.seek(loc * blockSize)
        return disk.read(blockSize)

def writeFile(data):
    loc = findEmptyBlock()
    saveBlock(loc, data)

def readFile(loc):
    result = bytearray()
    block = loadBlock(loc)
    while(block[0] != 0):
        for byte in block:
            result.append(byte)
        loc = loc + 1
        block = loadBlock(loc)
    return result
    

def findEmptyBlock():
    for a in range(blockNum):
        block = loadBlock(a)
        if block[0] != 0:
            return a
        
if __name__ == "__main__":
    fdisk()
