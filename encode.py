import diskUtils

def round(val):
    if(val - int(val) > 0):
        return int(val) + 1
    else:
        return int(val)


def encode(data):
    numBlocks = round(float(len(data)) / float(diskUtils.blockSize))
    checksum = bytearray(diskUtils.blockSize)
    for n in range(numBlocks):
        for b in range(diskUtils.blockSize):
            a = n * diskUtils.blockSize + b
            if a < len(data):
                checksum[b] ^= data[a]
            else:
                break
    return checksum

def decode(data, checksum):
    numBlocks = round(float(len(data)) / float(diskUtils.blockSize))
    tempCheckSum = bytearray(diskUtils.blockSize)
    for n in range(numBlocks):
        for b in range(diskUtils.blockSize):
            a = n * diskUtils.blockSize + b
            if a < len(data):
                tempCheckSum[b] ^= data[a]
            else:
                break
    for a in range(diskUtils.blockSize):
        tempCheckSum[a] ^= checksum[a]
    return tempCheckSum
    

if __name__ == "__main__":
    data = bytearray()
    with open ('mutualStore.py', 'rb') as file:
        byte = file.read(1)
        while(byte):
            data.append(byte[0])
            byte = file.read(1)
        file.close
    checksum = encode(data)

    data2 = bytearray()
    with open('mutualStore.py', 'rb') as file2:
        file2.seek(256)
        byte = file2.read(1)
        while(byte):
            data2.append(byte[0])
            byte = file2.read(1)
        file2.close
    
    print(decode(data2, checksum).decode('utf-8'))