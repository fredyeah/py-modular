from time import sleep
import threading
import sounddevice as sd
import numpy as np
import struct
import math
import random

class GlobalTransport:
    def __init__(self, nodes):
        self.nodes = nodes
        self.count = 0;
        self.buffer = []
    def add_node(self, node):
        self.nodes.append(node)
    def play_buffer(self):
        pass
    def get_block(self):
        self.buffer = []
        for i in range(512):
            sample = 0
            for node in self.nodes:
                s = node.get_sample()
                sample = (s + sample) / 2
            self.buffer.append(sample)
        return self.buffer
    def buffer_cb(self, indata, outdata, frames, time, status):
        block = self.get_block()
        arry = np.array(block).reshape((512, 1))
        outdata[:] = arry
    def begin_thread(self):
        while True:
            with sd.Stream(channels=1, callback=self.buffer_cb):
                sd.sleep(9375)
    def start(self):
        threading.Thread(target=self.begin_thread).start()

class VCO:
    def __init__(self, freq, gain, offset=0, freqct=None):
        self.freq = freq
        self.gain = gain
        self.offset = offset
        self.count = 0
        self.fs = 48000
        self.freqct = freqct
    def pitch_to(self, freq):
        self.freq = freq
    def gain_to(self, gain):
        self.gain = gain
    def get_sample(self):
        if not self.freqct == None:
            cv = self.freqct.get_sample()
            self.pitch_to(cv)
        pos = (self.count + 1) / self.fs
        value = math.sin(self.freq * 2.0 * math.pi * pos)
        value = value * self.gain + self.offset
        self.count = (self.count + 1) % self.fs
        return value

class Mixer:
    def __init__(self, nodes, gainct=None):
        self.nodes = nodes
        self.gainct = gainct
    def get_sample(self):
        sample = 0
        for node in self.nodes:
            sample = (sample + node.get_sample()) / 2
        if not self.gainct == None:
            sample = sample * self.gainct.get_sample()
        return sample

amp = VCO(0.1, 0.5, 0.5)
lfo = VCO(400, 10.0, 100.0)
vco = VCO(440, 0.8, 0, lfo)
vca = VCO(400, 1.0)
vcb = VCO(120, 1.0)
mx = Mixer([vca, vcb], amp)
gt = GlobalTransport([mx])
gt.start()
# gt.add_node(vco)

while True:
    f = input('lfo freq: ')
    lfo.pitch_to(f)
    # sleep(random.random() * 5)
    # a = random.random() * 200 + 60
    # b = random.random() * 200 + 60
    # a = int(a)
    # b = int(b)
    # vca.pitch_to(a)
    # vcb.pitch_to(b)


#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
