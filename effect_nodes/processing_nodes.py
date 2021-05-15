import math

class Filter:
    def __init__(self, node, coef=0.0):
        self.node = node
        self.coef = coef
        self.out_data = 0.0
    def get_sample(self, time):
        in_data = self.node.get_sample(time)
        self.out_data = self.out_data - (self.coef * (self.out_data - in_data))
        return self.out_data

class Lim:
    def __init__(self, node, th=1000.0, roll_off=100.0):
        self.node = node
        self.th = th
        self.last_value = 0.0
        self.roll_off = roll_off
    def get_sample(self, time):
        s = self.node.get_sample(time)
        self.last_value = (s + self.roll_off * self.last_value) / (self.roll_off + 1)
        value = math.atan(self.last_value * 3.0) * 2.0 / math.pi
        return value
