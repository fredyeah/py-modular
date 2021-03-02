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
    def __init__(self, len, curve_gain=1.0, curvect=None, roll_off=100.0):
        super().__init__(len)
        self.roll_off = roll_off
        self.curvect = curvect
        value = curve_gain * 0.999999
        self.last_value = 0.0
        if value > 0.0:
            self.curve_gain = -1.0 / (value - 1.0)
        else:
            self.curve_gain = value + 1
    def curve_gain_to(self, value):
        value = value * 0.999999
        if value > 0.0:
            self.curve_gain = -1.0 / (value - 1.0)
        else:
            self.curve_gain = value + 1
    def get_sample(self, time):
        t = time - self.start_time
        if t > (1.0 / self.len):
            self.triggered = False
            if not self.curvect == None:
                self.curve_gain_to(self.curvect.get_sample(time))
        if self.triggered == True:
            phase = self.len * math.pi * t + 0.5 * math.pi
            s = math.atan(math.tan(phase)) * -1.0 / math.pi + 0.5
            value = math.pow(s, self.curve_gain)
            self.last_value = (value + self.roll_off * self.last_value) / (self.roll_off + 1)
            return self.last_value
        else:
            return 0.0
