import math

class Mixer:
    def __init__(self, nodes, gain=1.0, gainct=None):
        self.nodes = nodes
        self.gain = float(gain)
        self.gainct = gainct
    def get_sample(self, time):
        sample = 0
        for node in self.nodes:
            sample = node.get_sample(time) + sample
        if not self.gainct == None:
            self.gain = self.gainct.get_sample(time)
        sample = sample / len(self.nodes)
        return sample * self.gain

class Atten:
    def __init__(self, node, gain=1.0, offset=0.0):
        self.node = node
        self.gain = gain
        self.offset = offset
    def get_sample(self, time):
        return self.node.get_sample(time) * self.gain + self.offset

class LinToExp:
    def __init__(self, node, curve_gain=1.0, curvect=None, log=False):
        self.node = node
        value = curve_gain * 0.999999
        if value > 0.0:
            self.curve_gain = -1.0 / (value - 1.0)
        else:
            self.curve_gain = value + 1
        self.curvect = curvect
        self.log = log
    def curve_gain_to(self, value):
        value = value * 0.999999
        if value > 0.0:
            self.curve_gain = -1.0 / (value - 1.0)
        else:
            self.curve_gain = value + 1
    def get_sample(self, time):
        if not self.curvect == None:
            self.curve_gain_to(self.curvect.get_sample(time))
        s = self.node.get_sample(time) * 0.5 + 0.5
        value = math.pow(s, self.curve_gain) - 0.5
        return value * 2.0
