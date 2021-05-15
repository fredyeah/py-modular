import random
import math

# RULES:
# an oscillator will output a wave between -1.0 and 1.0 by default
# gain and offset linearly scale the output of the oscillator
# one gain controller can be assigned to an oscillator which will linearly scale the gain
# one Array of fm controllers can be assigned to an oscillator which will linearly scale the frequency 

class Oscillator:
    def __init__(self, freq=100.0, gain=1.0, offset=0.0, gainct=None, fmct=None):
        self.freq = float(freq)
        self.gain = float(gain)
        self.offset = float(offset)
        self.gainct = gainct
        self.fmct = fmct
        self.phi = 0.0
    def gain_to(self, gain):
        self.gain = float(gain)
    def get_pcm_value(self, time):
        return 0.0
    def get_sample(self, time):
        if not self.fmct == None:
            for fm in self.fmct:
                self.phi = fm.get_sample(time) * 0.0001 + self.phi
        if not self.gainct == None:
            self.gain_to(self.gainct.get_sample(time))
        return self.get_pcm_value(time) * self.gain + self.offset

class Saw(Oscillator):
    def get_pcm_value(self, time):
        p = self.phi * 2.0 * math.pi
        phase = self.freq * math.pi * time
        value = math.atan(math.tan(phase + p)) * 2.0 / math.pi
        return value

class Sine(Oscillator):
    def get_pcm_value(self, time):
        p = self.phi * 2.0 * math.pi
        phase = self.freq * math.pi * 2.0 * time
        value = math.sin(phase + p)
        return value

class Tri(Oscillator):
    def get_pcm_value(self, time):
        p = self.phi * 2.0 * math.pi
        phase = self.freq * math.pi * 2.0 * time
        value = math.asin(math.sin(phase + p)) * 2.0 / math.pi
        return value

class Square(Oscillator):
    def __init__(self, freq=100.0, gain=1.0, offset=0.0, gainct=None, fmct=None, pwmct=None):
        super().__init__(freq, gain, offset, gainct, fmct)
        self.pwmct = pwmct
        self.th = 0.0
    def get_pcm_value(self, time):
        if not self.pwmct == None:
            self.th = self.pwmct.get_sample(time)
        p = self.phi * 2.0 * math.pi
        phase = self.freq * math.pi * 2.0 * time
        value = math.asin(math.sin(phase + p)) * 2.0 / math.pi
        if value > self.th:
            value = 1.0
        else:
            value = -1.0
        return value

class Random(Oscillator):
    def __init__(self, freq=100.0, gain=1.0, offset=0.0, gainct=None, fmct=None):
        super().__init__(freq, gain, offset, gainct, fmct)
        self.time_period = 1.0 / float(freq)
        self.start_time = 0.0
        self.start_value = 0.0
        self.end_value = (random.random() - 0.5) * 2.0
        self.range = self.end_value - self.start_value
    def start_cycle(self, time):
        self.start_time = time
        self.start_value = self.end_value
        self.end_value = (random.random() - 0.5) * 2.0
        self.range = self.end_value - self.start_value
    def get_pcm_value(self, time):
        t = time - self.start_time
        phase = t / self.time_period
        value = self.range * phase + self.start_value
        if phase >= 1.0:
            self.start_cycle(time)
        return value
