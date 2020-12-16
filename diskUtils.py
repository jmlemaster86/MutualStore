blockSize = 1024
blockNum = 10
diskSize = blockSize * blockNum


#creates a virtual disk of diskSize
def fdisk():
    with open('disk.bin', 'wb') as disk:
        disk.write(bytearray(diskSize))

#saves data at location loc on the virtual disk
def saveBlock(loc, data):
    with open('disk.bin', 'r+b') as disk:
        disk.seek(loc * blockSize)
        disk.write(data)
        
#loads data from a location on disk
def loadBlock(loc):
    with open('disk.bin', 'rb') as disk:
        disk.seek(loc * blockSize)
        return disk.read(blockSize)

#unused
def writeFile(data):
    loc = findEmptyBlock()
    saveBlock(loc, data)

#unused
def readFile(loc):
    result = bytearray()
    block = loadBlock(loc)
    while(block[0] != 0):
        for byte in block:
            result.append(byte)
        loc = loc + 1
        block = loadBlock(loc)
    return result
    
#unused
def findEmptyBlock():
    for a in range(blockNum):
        block = loadBlock(a)
        if block[0] != 0:
            return a
        
if __name__ == "__main__":
    fdisk()