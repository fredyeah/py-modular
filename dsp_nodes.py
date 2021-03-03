class Delay:
    def __init__(self, nodes, len, fb):
        self.nodes = nodes
        self.len = len
        self.buffer = [0.0] * len
        self.txrx = 0
        self.fb = fb
    def add_input(self, node):
        self.nodes.append(node)
    def get_sample(self, time):
        samp = 0.0
        for node in self.nodes:
            samp = node.get_sample(time) + samp
        samp = samp / len(self.nodes)
        samp = (samp + self.buffer[self.txrx] * self.fb) / 1.5
        value = self.buffer[self.txrx]
        self.buffer[self.txrx] = samp
        self.txrx = (self.txrx + 1) % self.len
        return value

class MultiTapDelay:
    def __init__(self, node, taps=[]):
        self.node = node
        self.taps = taps
        self.buffer = [0] * 48000
        self.count = 0
    def get_sample(self, time):
        self.buffer[self.count] = self.node.get_sample(time)
        samp = 0.0
        for i in range(len(self.taps)):
            samp = samp + self.buffer[self.taps[i]]
            self.taps[i] = (self.taps[i] + 1) % len(self.buffer)
        samp = samp / len(self.taps)
        self.buffer[self.count] = (self.node.get_sample(time) + samp * 1.4) / 1.5
        self.count = (self.count + 1) % len(self.buffer)
        return (self.node.get_sample(time) + samp * 1.4) / 1.5

class Channel:
    def __init__(self, parent):
        self.value = 0.0
        self.parent = parent
        pass
    def get_sample(self, time):
        value = self.parent.get_sample(time)
        return value

class MultiChannelDelay:
    def __init__(self, nodes, len, fb):
        self.nodes = nodes
        self.len = [
            len[0],
            len[1]
        ]
        self.buffer = [
            [0.0] * len[0],
            [0.0] * len[1]
        ]
        self.txrx = [0, 0]
        self.fb = fb
        self.ch_num = 0
    def add_input(self, node):
        self.nodes.append(node)
    def get_sample(self, time):
        samp = 0.0
        for node in self.nodes:
            samp = node.get_sample(time) + samp
        samp = samp / len(self.nodes)
        c_n = self.ch_num
        samp = (samp + self.buffer[c_n][self.txrx[c_n]] * self.fb) / 1.5
        value = self.buffer[c_n][self.txrx[c_n]]
        self.buffer[c_n][self.txrx[c_n]] = samp
        self.txrx[c_n] = (self.txrx[c_n] + 1) % self.len[c_n]
        self.ch_num = (self.ch_num + 1) % len(self.buffer)
        return value
