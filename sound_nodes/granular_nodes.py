from random import randint, random

class GranBase:
    def __init__(self, grains, freq=20.0, gain=1.0, offset=0.0, gainct=None):
        self.grains = grains
        self.num_grains = len(grains)
        self.current_grain = 0
        self.playing_grains = [0]
        self.grain_positions = [0] * self.num_grains
        self.freq = float(freq)
        self.freq_in_seconds = 1.0 / self.freq
        self.time = 0.0
        self.gain = float(gain)
        self.offset = float(offset)
        self.gainct = gainct
        self.phi = 0.0
    def gain_to(self, gain):
        self.gain = float(gain)
    def freq_to(self, freq):
        self.freq = float(freq)
        self.freq_in_seconds = 1.0 / self.freq
    def fire_grain(self):
        self.current_grain = (self.current_grain + 1) % self.num_grains
        self.playing_grains.append(self.current_grain)
        self.freq_to(random() * 10.0 + 20.0)
    def get_pcm_value(self, time):
        values = []
        for grain in self.playing_grains:
            self.grain_positions[grain] = self.grain_positions[grain] + 1
            if(self.grain_positions[grain] >= len(self.grains[grain])):
                self.playing_grains.remove(grain)
                self.grain_positions[grain] = 0
            values.append(self.grains[grain][self.grain_positions[grain]])
        if(len(values) > 0):
            return sum(values) / len(values)
        return 0.0
    def get_sample(self, time):
        # time = time + (random() * -0.000001)
        if not self.gainct == None:
            self.gain_to(self.gainct.get_sample(time))
        if self.time > (time % self.freq_in_seconds):
            # fire grain
            self.fire_grain()
        self.time = time % self.freq_in_seconds
        return self.get_pcm_value(time) * self.gain + self.offset
