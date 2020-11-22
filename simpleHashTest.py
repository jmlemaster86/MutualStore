import hashlib

def hash(value):
    return int(hashlib.sha1(value).hexdigest()[:8], 16) % 256

if __name__ == "__main__":
    for a in range(100):
        print(hash(str(a)))
