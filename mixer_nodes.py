class Mixer:
    def __init__(self, nodes, gainct=None):
        self.nodes = nodes
        self.gainct = gainct
    def get_sample(self, time):
        sample = 0
        for node in self.nodes:
            sample = node.get_sample(time)
        sample = sample / len(self.nodes)
        return sample

class Atten:
    def __init__(self, node, gain=1.0, offset=0.0):
        self.node = node
        self.gain = gain
        self.offset = offset
    def get_sample(self, time):
        return self.node.get_sample(time) * self.gain + self.offset
