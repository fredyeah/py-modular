import math

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
