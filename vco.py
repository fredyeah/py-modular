from time import sleep
import threading
import sounddevice as sd
import numpy as np
import struct
import math
import random
import matplotlib.pyplot as plot

class GlobalTransport:
    def __init__(self, nodes, buffer_len=1024):
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
            with sd.Stream(channels=1, samplerate=48000, blocksize=1024, callback=self.buffer_cb):
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
        self.freq = float(48000/freq)
        self.gain = float(gain)
        self.offset = float(offset)
        self.count = 0
        self.fs = 48000
        self.freqct = freqct
        self.gainct = gainct
        self.fmct = fmct
    def pitch_to(self, freq):
        self.freq = float(48000/freq)
    def gain_to(self, gain):
        self.gain = gain
    def get_sample(self):
        if not self.freqct == None:
            self.pitch_to(self.freqct.get_sample())
        fmcv = 0.0
        if not self.fmct == None:
            for fm in self.fmct:
                fmcv = fmcv + fm.get_sample()
        value = ((self.count + fmcv) % self.freq) / self.freq
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
    def amp_to(self, amp):
        self.amp = amp
    def get_sample(self):
        val = self.node.get_sample()
        if val < 0.000001:
            val = 0.000001
        if val > 1:
            val = 1
        val = (math.pow(self.amp, val) - 1) / (0.9 * self.amp)
        return val

class Atten:
    def __init__(self, node, gain=1.0, offset=0.0):
        self.node = node
        self.gain = gain
        self.offset = offset
    def get_sample(self):
        return self.node.get_sample() * self.gain + self.offset

class Envelope:
    def __init__(self, len, gatect=None):
        self.len = 48000.0 / len
        self.count = 0
        self.step = 1 / self.len
        self.playing = False
        self.gatect = gatect
    def trigger(self):
        self.playing = True
    def get_sample(self):
        # if not self.gatect == None:
        #     s = self.gatect.get_sample()
        #     if s < self.lth:
        #         self.last_lth = s
        #     if s > self.hth:
        #         self.last_hth = s
        value = 0.0
        if self.playing == True:
            value = 1 - self.count * self.step
            self.count = self.count + 1
            if self.count >= self.len:
                self.playing = False
                self.count = 0;
        return value

class Trigger:
    def __init__(self, len):
        pass

class Delay:
    def __init__(self, node, len):
        self.node = node
        self.len = len
        self.buffer = [0.0] * len
        self.txrx = 0
    def get_sample(self):
        samp = (self.node.get_sample() + self.buffer[self.txrx]) / 2.0
        value = self.buffer[self.txrx]
        self.buffer[self.txrx] = samp
        self.txrx = (self.txrx + 1) % self.len
        return value

class Mult:
    def __init__(self, node=None):
        self.node = node
        self.flip = False
        self.value = 0.0
    def get_sample(self):
        if self.flip == True:
            self.value = self.node.get_sample()
        else:
            pass
        self.flip = not self.flip
        return self.value

class Filter:
    def __init__(self, node, coef=0.0):
        self.node = node
        self.coef = coef
        self.out_data = 0.0
    def get_sample(self):
        in_data = self.node.get_sample()
        self.out_data = self.out_data - (self.coef * (self.out_data - in_data))
        return self.out_data


# rand = Random(48000, 500, 100)
# op = Random(48000, 1, 0.5)
# amp = VCO(0, 1.0, 5)
# rfreq = Random(freq=48000, gain=500, offset=400)
# ctl = VCO(100, 5, gainct=op, fmct=[rand])
# am = Random(freq=10000, gain=10, offset=390)
# grh = VCO(300.0, 1, fmct=[ctl, rfreq, am])
# env = Mixer([grh], amp)

# ctl = VCO(0.1, 10000, 11000)
rnc = Random(4000)
att = Atten(rnc, 20000.0, 20000.1)
saw = Saw(1, -1.0, 1.0, fmct=[att])
en = Envelope(1.3)
conv = LinToExp(en, 1000.0)
# log = Random(4800)
#
#
# con = LinToLog(log, 1.0)
env = LinToExp(saw, 10.0)


osc = VCO(freq=200, gainct=conv, fmct=[VCO(freq=0.254, gain=150.0, offset=200.0), Atten(Random(100000), 100.0, 200.0), VCO(freq=220, fmct=[Random(10000)])])

# graph_node(ctl, 48000 * 1)
# graph_node(saw, 48000 * 1)
# graph_node(env, 48000 * 3)
en.trigger()
# graph_node(conv, 48000 * 1)

mult = Mult(osc)
dly = Delay(Delay(Delay(mult, 30009), 798), 120)

master = Mixer([mult, dly])
COEF = 0.12
fil = Filter(Filter(Filter(Filter(master, COEF), COEF), COEF), COEF)


gt = GlobalTransport([fil])
gt.start()

while True:
    sleep(random.random() * 3)
    en.trigger()

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
