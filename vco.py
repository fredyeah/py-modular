from time import sleep
import threading
import sounddevice as sd
import numpy as np
import struct
import math
import random
import matplotlib.pyplot as plot

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
    def __init__(self, freq, gain, offset=0, freqct=None, gainct=None):
        self.freq = float(freq)
        self.gain = float(gain)
        self.offset = float(offset)
        self.count = 0
        self.fs = 48000
        self.freqct = freqct
        self.gainct = gainct
    def pitch_to(self, freq):
        self.freq = freq
    def gain_to(self, gain):
        self.gain = gain
    def get_sample(self):
        freqcv = 0.0
        if not self.freqct == None:
            freqcv = self.freqct.get_sample()
        if not self.gainct == None:
            gaincv = self.gainct.get_sample()
            self.gain_to(gaincv)
        pos = (self.count + 1) / self.fs
        value = math.sin(freqcv + self.freq * 2.0 * math.pi * pos)
        value = value * self.gain + self.offset
        self.count = (self.count + 1)
        return value

def graph_node(node, samples):
    time = []
    samps = []
    for i in range(samples):
        sample = node.get_sample()
        samps.append(sample)
        time.append(i)
    plot.plot(time, samps)
    plot.title('Sine wave')
    plot.xlabel('Time')
    plot.ylabel('Amplitude = sin(time)')
    plot.grid(True, which='both')
    plot.axhline(y=0, color='k')
    plot.show()
    plot.show()

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

amp = VCO(0.5, 0.1, 0.9)
op = VCO(0.2, 1)
ctl = VCO(100, 5, gainct=op)
grh = VCO(300.0, 1, freqct=ctl)
env = Mixer([grh], amp)

# graph_node(env, 4800)

gt = GlobalTransport([env])
gt.start()


while True:
    sleep(random.random() * 5)
    r = random.random() * 200 + 60
    grh.pitch_to(r)


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
