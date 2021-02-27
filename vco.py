from time import sleep
import threading
import sounddevice as sd
import numpy as np
import struct
import math
import random
import matplotlib.pyplot as plot

class GlobalTransport:
    def __init__(self, nodes, buffer_len=512):
        self.buffer_len = buffer_len
        self.nodes = nodes
        self.count = 0;
        self.buffer = []
    def add_node(self, node):
        self.nodes.append(node)
    def play_buffer(self):
        pass
    def get_block(self):
        self.buffer = []
        for i in range(self.buffer_len):
            sample = 0
            for node in self.nodes:
                s = node.get_sample()
                sample = (s + sample) / 2
            self.buffer.append(sample)
        return self.buffer
    def buffer_cb(self, indata, outdata, frames, time, status):
        block = self.get_block()
        arry = np.array(block).reshape((self.buffer_len, 1))
        outdata[:] = arry
    def begin_thread(self):
        while True:
            with sd.Stream(channels=1, callback=self.buffer_cb):
                sd.sleep(int((48000 / self.buffer_len) * 1000))
    def start(self):
        threading.Thread(target=self.begin_thread).start()

class VCO:
    def __init__(self, freq=100.0, gain=1.0, offset=0.0, freqct=None, gainct=None, fmct=None):
        self.freq = float(freq)
        self.gain = float(gain)
        self.offset = float(offset)
        self.count = 0
        self.fs = 48000
        self.freqct = freqct
        self.gainct = gainct
        self.fmct = fmct
    def pitch_to(self, freq):
        self.freq = freq
    def gain_to(self, gain):
        self.gain = gain
    def get_sample(self):
        fmcv = 0.0
        if not self.freqct == None:
            f = self.freqct.get_sample()
            self.pitch_to(f)
        if not self.fmct == None:
            for fm in self.fmct:
                fmcv = fmcv + fm.get_sample()
            # fmcv = self.fmct.get_sample()
        if not self.gainct == None:
            gaincv = self.gainct.get_sample()
            self.gain_to(gaincv)
        pos = (self.count + 1) / self.fs
        value = math.sin(fmcv + self.freq * 2.0 * math.pi * pos)
        value = value * self.gain + self.offset
        self.count = (self.count + 1)
        return value

class Saw:
    def __init__(self, freq=100.0, gain=1.0, offset=0.0, freqct=None, gainct=None, fmct=None):
        self.freq = float(freq)
        self.gain = float(gain)
        self.offset = float(offset)
        self.count = 0
        self.fs = 48000
        self.freqct = freqct
        self.gainct = gainct
        self.fmct = fmct
    def pitch_to(self, freq):
        self.freq = freq
    def gain_to(self, gain):
        self.gain = gain
    def get_sample(self):
        value = (self.count % self.freq) / self.freq
        value = value * self.gain + self.offset
        self.count = (self.count + 1)
        return value

class Random:
    def __init__(self, freq):
        self.fs = 48000
        self.count = 0
        self.freq = float(freq)
        self.start_val = self.get_value()
        self.end_val = self.get_value()
        self.step_val = (self.end_val - self.start_val) / self.freq
    def get_value(self):
        return random.random()
    def next_value(self):
        self.start_val = self.end_val
        self.end_val = self.get_value()
        self.step_val = (self.end_val - self.start_val) / self.freq
    def get_sample(self):
        value = self.start_val + (self.step_val * self.count)
        self.count = (self.count + 1) % self.freq
        if self.count == 0:
            self.next_value()
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
    # plot.yscale('log')
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

class LinToLog:
    def __init__(self, node, amp=1.0, offset=0.0):
        self.node = node
        self.amp = amp
        self.offset = offset
    def get_sample(self):
        val = self.node.get_sample()
        if val < 0.000001:
            val = 0.000001
        if val > 1:
            val = 1
        # val = (10 * math.log10(val+0.0) + 60.0) / 60.0
        # val = (10 * math.log10(val+2.0) + 0.0) / 0.0
        val = (10 * math.log10(val+0.0) + 60.0) / 60.0
        # val = val * self.amp + self.offset
        return val

class LinToExp:
    def __init__(self, node, amp=1.0, offset=0.0):
        self.node = node
        self.amp = amp * 10.0
        self.offset = offset
    def get_sample(self):
        val = self.node.get_sample()
        if val < 0.000001:
            val = 0.000001
        if val > 1:
            val = 1
        val = (math.pow(self.amp, val) - 1) / (0.9 * self.amp)
        return val

# rand = Random(48000, 500, 100)
# op = Random(48000, 1, 0.5)
# amp = VCO(0, 1.0, 5)
# rfreq = Random(freq=48000, gain=500, offset=400)
# ctl = VCO(100, 5, gainct=op, fmct=[rand])
# am = Random(freq=10000, gain=10, offset=390)
# grh = VCO(300.0, 1, fmct=[ctl, rfreq, am])
# env = Mixer([grh], amp)

saw = Saw(48000, -1.0, 1.0)
# log = Random(4800)
#
#
# con = LinToLog(log, 1.0)
env = LinToExp(saw, 1000000.0)

osc = VCO(freq=200, gainct=env)

# graph_node(env, 48000 * 3)
# graph_node(saw, 48000 * 3)

gt = GlobalTransport([osc])
gt.start()

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
