from random import randint, random
from math import floor, asin, sin, pi

class GranBase:
    def __init__(self, grains, freq=10.0, jitter=0, random_offset=0, grain_range=[None, None], gain=1.0, offset=0.0, gainct=None):
        self.grains = grains
        self.num_grains = len(grains)
        self.current_grain = 0
        self.playing_grains = [0]
        self.grain_positions = [0] * self.num_grains
        self.freq = float(freq)
        self.freq_in_seconds = 1.0 / self.freq
        self.jitter = float(jitter)
        self.random = random_offset
        self.time = 0.0
        self.gain = float(gain)
        self.offset = float(offset)
        self.gainct = gainct
        self.phi = 0.0
    def gain_to(self, gain):
        self.gain = float(gain)
    def make_jitter(self):
        self.freq_in_seconds = 1.0 / (self.freq + (random() - 0.5) * self.jitter)
    def fire_grain(self):
        self.current_grain = (self.current_grain + 1 + floor(random() * self.random)) % self.num_grains
        self.playing_grains.append(self.current_grain)
        print(self.playing_grains)
        self.make_jitter()
        print('grain fired ' + str(self.current_grain))
    def get_pcm_value(self, time):
        values = []
        for grain in self.playing_grains:
            self.grain_positions[grain] = self.grain_positions[grain] + 1
            if(self.grain_positions[grain] >= len(self.grains[grain])):
                self.playing_grains.remove(grain)
                self.grain_positions[grain] = 0
                self.fire_grain()
            values.append(self.grains[grain][self.grain_positions[grain]])
        if(len(values) > 0):
            return sum(values) / len(values)
        return 0.0
    def get_sample(self, time):
        # self.make_jitter()
        if not self.gainct == None:
            self.gain_to(self.gainct.get_sample(time))
        if self.time > (time % self.freq_in_seconds):
            # self.fire_grain()
            pass
        self.time = time % self.freq_in_seconds
        return self.get_pcm_value(time) * self.gain + self.offset

def window_grains_sin(grains=[]):
    for grain in grains:
        grain_length = len(grain)
        for i in range(grain_length):
            grain[i] = grain[i] * sin(i * pi / grain_length)
    return grains

def window_grains_tri(grains=[]):
    for grain in grains:
        grain_length = len(grain)
        for i in range(grain_length):
            grain[i] = grain[i] * (asin(sin(i * pi / grain_length)) / (0.5 * pi))
    return grains
