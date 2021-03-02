import math

class Envelope:
    def __init__(self, len):
        self.len = float(len)
        self.triggered = False
        self.start_time = 0.0
    def trigger(self, time):
        self.triggered = True
        self.start_time = time
    def get_sample(self, time):
        t = time - self.start_time
        if t > (1.0 / self.len):
            self.triggered = False
        if self.triggered == True:
            phase = self.len * math.pi * t + 0.5 * math.pi
            return math.atan(math.tan(phase)) * -1.0 / math.pi + 0.5
        else:
            return 0.0

class ExpEnv(Envelope):
    def __init__(self, len, curve_gain=1.0):
        super().__init__(len)
        value = curve_gain * 0.999999
        if value > 0.0:
            self.curve_gain = -1.0 / (value - 1.0)
        else:
            self.curve_gain = value + 1
    def get_sample(self, time):
        t = time - self.start_time
        if t > (1.0 / self.len):
            self.triggered = False
        if self.triggered == True:
            phase = self.len * math.pi * t + 0.5 * math.pi
            s = math.atan(math.tan(phase)) * -1.0 / math.pi + 0.5
            value = math.pow(s, self.curve_gain)
            return value
        else:
            return 0.0
