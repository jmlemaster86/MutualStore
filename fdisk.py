

def fdisk():
    with open('disk.bin', 'wb') as disk:
        disk.write(bytearray(10485760))

if __name__ == '__main__':
    fdisk()
