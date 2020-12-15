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


if __name__ == "__main__":
    data = bytearray()
    with open ('mutualStore.py', 'rb') as file:
        byte = file.read(1)
        while(byte):
            data.append(byte[0])
            byte = file.read(1)
    checksum = encode(data)
    print(checksum.decode('utf-8'))