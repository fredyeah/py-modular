

class GranBase:
    def __init__(self, grains, freq=0.8, gain=1.0, offset=0.0, gainct=None):
        self.grains = grains
        self.num_grains = len(grains)
        self.current_grain = 0
        self.freq = float(freq)
        self.freq_in_seconds = 1.0 / self.freq
        self.time = 0.0
        self.gain = float(gain)
        self.offset = float(offset)
        self.gainct = gainct
        self.phi = 0.0
    def gain_to(self, gain):
        self.gain = float(gain)
    def fire_grain(self):
        self.current_grain = (self.current_grain + 1) % self.num_grains
        print(self.current_grain)
    def get_pcm_value(self, time):
        return 0.0
    def get_sample(self, time):
        if not self.gainct == None:
            self.gain_to(self.gainct.get_sample(time))
        if self.time > (time % self.freq_in_seconds):
            # fire grain
            self.fire_grain()
        self.time = time % self.freq_in_seconds
        return self.get_pcm_value(time) * self.gain + self.offset
