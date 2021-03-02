class Delay:
    def __init__(self, node, len, fb):
        self.node = node
        self.len = len
        self.buffer = [0.0] * len
        self.txrx = 0
        self.fb = fb
    def get_sample(self, time):
        samp = (self.node.get_sample(time) + self.buffer[self.txrx] * self.fb) / 1.5
        value = self.buffer[self.txrx]
        self.buffer[self.txrx] = samp
        self.txrx = (self.txrx + 1) % self.len
        return value
