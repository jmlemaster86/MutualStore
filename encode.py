
class encoder():

    def __init__(self, w):
        prim_poly = 0
        if w == 4:
            prim_poly = 23
        elif w == 8:
            prim_poly = 435
        elif w == 16:
            prim_poly = 210013
            

        self.x_to_w = 2**w
        self.gflog = [0] * self.x_to_w
        self.gfilog = [0] * self.x_to_w
        
        b = 1
        for log in range(x_to_w):
            self.gflog[b] = log
            self.gfilog[log] = b
            b = b << 1
            if(b & x_to_w):
                b = b ^ prim_poly

    def add_sub(self, a, b):
        return a ^ b

    def multi(self, a, b):
        if a == 0 or b == 0:
            return 0
        sum_log = self.gflog[a] + self.gflog[b]
        if sum_log >= self.x_to_w - 1:
            sum_log -= self.x_to_w - 1
        return self.gfilog[sum_log]

    def div(self, a, b):
        if a == 0:
            return 0
        if b == 0:
            return -1
        diff_log = self.gflog[a] - self.gflog[b]
        if diff_log < 0:
            diff_log += self.x_to_w
        return self.gfilog[diff_log]

    def encode(self, data):
        

if __name__ == "__main__":