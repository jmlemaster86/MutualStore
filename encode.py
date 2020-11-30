
def encode(data):
    resultBuffer = bytearray()
    currentByte = 0
    count = 0
    for byte in data:
        if(count % 2 == 0):
            count = count + 1
            currentByte = byte
            continue
        resultBuffer.append(byte)
        resultBuffer.append(xor(currentByte, byte))
        currentByte = byte
        count = count + 1
    return resultBuffer

def xor(a, b):
    c = (a | b) & ~(a & b)
    print(str(a) + ' XOR ' + str(b) + ' = ' + str(c))
    return c

if __name__ == "__main__":
    text = [1, 2, 3, 4, 5]
    data = bytearray(text)
    encode(data)
