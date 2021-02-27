from time import sleep
import threading
import sounddevice as sd
import soundfile as sf
import numpy as np
import struct
import math
import random
import matplotlib.pyplot as plot

BUFFER_SIZE = 2048
TEST_FILE = []

class GlobalTransport:
    def __init__(self, nodes, buffer_len=BUFFER_SIZE):
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
            TEST_FILE.append(sample)
        return self.buffer
    def buffer_cb(self, indata, outdata, frames, time, status):
        block = self.get_block()
        arry = np.array(block).reshape((self.buffer_len, 1))
        outdata[:] = arry
    def begin_thread(self):
        while True:
            with sd.Stream(channels=1, samplerate=48000, blocksize=BUFFER_SIZE, callback=self.buffer_cb):
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
        theta = 0.0
        if not self.freqct == None:
            f = self.freqct.get_sample()
            theta = (1 / f) * 2 * math.pi
            self.pitch_to(f)
        if not self.fmct == None:
            for fm in self.fmct:
                fmcv = fmcv + fm.get_sample()
            # fmcv = self.fmct.get_sample()
        if not self.gainct == None:
            gaincv = self.gainct.get_sample()
            self.gain_to(gaincv)
        pos = (self.count + 1) / self.fs
        value = math.sin(fmcv + theta + self.freq * 2.0 * math.pi * pos)
        value = value * self.gain + self.offset
        self.count = (self.count + 1)
        return value

# math.sin(theta + self.freq * 2.0 * math.pi * pos) = sin(theta)cos(2pixf) + cos(theta)sin(2pixf)
# sin(theta)cos(2pixf) = cos(theta)sin(2pixf)
# cos(2pixf)/sin(2pixf) = cos(theta)/sin(theta)
# cot(2pixf) = cot(theta)




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

def record_file(node, seconds=5):
    buffer = []
    for i in range(48000 * seconds):
        # if (i % int((random.random() + 0.0001) * 48000 * 3)) == 0:
        #     en.trigger()
        samp = node.get_sample() / 10.0
        buffer.append(samp)
    sf.write('TEST_FILE.wav', buffer, 48000)

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
        samp = (self.node.get_sample() + self.buffer[self.txrx] * 1.5) / 1.55
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

class Lim:
    def __init__(self, node):
        self.node = node
    def get_sample(self):
        s = self.node.get_sample()
        if s > 1.0:
            s = 1.0
        if s < -1.0:
            s = -1.0
        return s

en = Envelope(1.3)
conv = LinToExp(en, 1000.0)

osc = VCO(freq=300, gainct=conv, fmct=[
        VCO(freq=0.254, gain=150.0, offset=200.0),
        Atten(Random(100000), 100.0, 200.0),
        VCO(freq=220, fmct=[Random(10000)])
    ])

en.trigger()
# graph_node(conv, 48000 * 1)

mult = Mult(osc)
dly = Delay(Delay(Delay(mult, 309), 798), 120)

master = Mixer([mult, dly])
COEF = 0.12
fil = Filter(Filter(Filter(Filter(master, COEF), COEF), COEF), COEF)

pitch = Envelope(1)
penv = LinToExp(pitch, 10000.0)
fenv = Atten(penv, gain=1000, offset=1001)
pitch.trigger()

ctl = Mult(fenv)

kick = VCO(freq=0,
    # gainct=LinToExp(
    #     Saw(freq=3, gain=-1.0, offset=1.0), 100.0
    # ),
    gainct=ctl,
    freqct=ctl
)

graph_node(kick, 48000)


tp = GlobalTransport([kick])
tp.start()






# gt = GlobalTransport([fil])
# gt.start()

# while True:
#     sleep(random.random() * 3)
#     osc.pitch_to(random.random() * 200 + 200)
#     en.trigger()
    # if input('write: ') == 'true':
    #
    #     exit()

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
