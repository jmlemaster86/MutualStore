import diskUtils

#used to round up to the nearest whole block
def round(val):
    if(val - int(val) > 0):
        return int(val) + 1
    else:
        return int(val)

#Creates a checksum block for rebuilding any missing data
def encode(data):
    #Gets the number of blocks for this file
    numBlocks = round(float(len(data)) / float(diskUtils.blockSize))
    checksum = bytearray(diskUtils.blockSize)
    #Iterates through each block
    for n in range(numBlocks):
        #Iterates through each byte
        for b in range(diskUtils.blockSize):
            #a is used to keep track of position in data
            a = n * diskUtils.blockSize + b
            #If not at the end of file
            if a < len(data):
                # xor's checksum byte b with byte b of block n of data
                checksum[b] ^= data[a]
            else:
                #breaks if at eof
                break
    #returns the resulting checksum
    return checksum

#takes a file and a checksum to calculate a missing block of data
def decode(data, checksum):
    #calcs the number of blocks of the source file
    numBlocks = round(float(len(data)) / float(diskUtils.blockSize))
    #temp storage for the missing block
    tempCheckSum = bytearray(diskUtils.blockSize)
    #process identical to the encoding process
    for n in range(numBlocks):
        for b in range(diskUtils.blockSize):
            a = n * diskUtils.blockSize + b
            if a < len(data):
                tempCheckSum[b] ^= data[a]
            else:
                break
    #now xor the tempCheckSum with checksum to restore the missing block
    for a in range(diskUtils.blockSize):
        tempCheckSum[a] ^= checksum[a]
    return tempCheckSum
    
#test code, please disregard
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