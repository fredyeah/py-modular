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
        self.lastp = 0.0

        self.phi = 0.0
        self.f0 = freq
        self.f1 = freq
    def pitch_to(self, freq):
        self.freq = freq
    def gain_to(self, gain):
        self.gain = gain
    def get_phase(self):
        f = 48000 / self.freq
        value = ((self.count) % f) / f
        # print(value - self.lastp, f)
        self.lastp = value
        print(value)
        return value
        # phase = (position / period )* 2pi
        # position = samp_counter / freq(samples/second)
        #
        # period = freq(samples/second)
    def get_sample(self):
        # new_freq = 0.0
        # if not self.freqct == None:
        #     new_freq = self.freqct.get_sample()
        # value = math.sin((self.freq + 1000 * new_freq) * 2.0 * math.pi * (self.count / self.fs) - self.freqct.get_phase() * 2 * math.pi)
        # self.count = self.count + 1
        # return value
        self.f1 = self.freq * self.freqct.get_sample()
        interval = 1.0 / 48000.0
        delta = 2 * math.pi * self.freq / self.fs
        f_delta = (self.f1 - self.f0) / (self.fs * interval)
        self.phi = self.phi + delta
        # self.freq = self.freq + f_delta
        # delta = 2 * math.pi * f / self.fs
        self.f0 = self.f1
        output = math.sin(self.freq * 2.0 * math.pi * self.phi)
        return output


# phi = 0;                      // phase accumulator
# f = f0;                       // initial frequency
# delta = 2 * pi * f / Fs;      // phase increment per sample
# f_delta = (f1 - f0) / (Fs * T_sweep);
#                               // instantaneous frequency increment per sample
# for each sample
#     output = A * sin(phi);    // output sample value for current sample
#     phi += delta;             // increment phase accumulator
#     f += f_delta;             // increment instantaneous frequency
#     delta = 2 * pi * f / Fs;  // re-calculate phase increment



# math.sin(theta + self.freq * 2.0 * math.pi * pos) = sin(theta)cos(2pixf) + cos(theta)sin(2pixf)
# sin(theta)cos(2pixf) = cos(theta)sin(2pixf)
# cos(2pixf)/sin(2pixf) = cos(theta)/sin(theta)
# cot(2pixf) = cot(theta)




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
        self.fmcv = 0.0
    def pitch_to(self, freq):
        self.freq = float(48000/freq)
    def gain_to(self, gain):
        self.gain = gain
    def get_phase(self):
        # phase = (position / period )* 2pi
        # position = samp_counter / freq(samples/second)
        #
        # period = freq(samples/second)
        return math.atan(math.tan(self.freq * math.pi * (self.count + 1) / self.fs)) * 2 / math.pi
    def get_sample(self):
        if not self.freqct == None:
            self.pitch_to(self.freqct.get_sample())
        if not self.fmct == None:
            for fm in self.fmct:
                self.fmcv = (self.fmcv + ((fm.get_sample()) * 0.00001))
        pos = (self.count) / self.fs
        value = math.atan(math.tan(self.freq * math.pi * pos + 0.5 * math.pi + 2 * math.pi * self.fmcv)) * 2 / math.pi
        value = value * self.gain + self.offset
        self.count = (self.count + 1)
        return value

class Sine:
    def __init__(self, freq=100.0, gain=1.0, offset=0.0, freqct=None, gainct=None, fmct=None):
        self.freq = float(freq)
        self.gain = float(gain)
        self.offset = float(offset)
        self.count = 0
        self.fs = 48000
        self.freqct = freqct
        self.gainct = gainct
        self.fmct = fmct
        self.fmcv = 0.0
    def pitch_to(self, freq):
        self.freq = float(48000/freq)
    def gain_to(self, gain):
        self.gain = gain
    def get_phase(self):
        return (self.count + 1) / self.fs
    def get_sample(self):
        # if not self.freqct == None:
        #     self.pitch_to(self.freqct.get_sample())
        if not self.gainct == None:
            self.gain_to(self.gainct.get_sample())
        if not self.fmct == None:
            for fm in self.fmct:
                self.fmcv = (self.fmcv + ((fm.get_sample()) * 0.00001))
        phi = 1.0
        if not self.freqct == None:
            phi = self.freqct.get_sample()
        pos = self.count / self.fs
        value = math.sin(self.freq * 2 * math.pi * pos + 2 * math.pi * self.fmcv)
        value = value * self.gain + self.offset
        self.count = self.count + 1
        return value

# value = math.sin(f * 2pi * pos)
# arcsin(value - p) = f * 2pi * pos
# 2pi * pos * arcsin(value) = f

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
    def __init__(self, node, len, fb):
        self.node = node
        self.len = len
        self.buffer = [0.0] * len
        self.txrx = 0
        self.fb = fb
    def get_sample(self):
        samp = (self.node.get_sample() + self.buffer[self.txrx] * self.fb) / 1.5
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

# en.trigger()
# # graph_node(conv, 48000 * 1)
#
# mult = Mult(osc)
# # dly = Delay(Delay(Delay(mult, 309), 798), 120)
#
# master = Mixer([mult, dly])
# COEF = 0.12
#
#
# pitch = Envelope(1)
# penv = LinToExp(pitch, 10000.0)
# fenv = Atten(penv, gain=1000, offset=1001)
# pitch.trigger()
#
# ctl = Mult(fenv)

# kick = VCO(freq=0,
#     # gainct=LinToExp(
#     #     Saw(freq=3, gain=-1.0, offset=1.0), 100.0
#     # ),
#     gainct=ctl,
#     freqct=ctl
# )

# fil = Filter(Filter(Filter(Filter(Saw(freq=7), COEF), COEF), COEF), COEF)

integrator = VCO(freq=10,
    freqct=Saw(freq=2.34)
)

# graph_node(VCO(freq=90, fmct=[Saw(freq=176)]), 48000)
# graph_node(VCO(freq=10), 48000)
# graph_node(Saw(freq=1), 48000)

class Transient:
    def __init__(self):
        self.f_start = 1.0
        self.f_end = 10.0
        self.fs = 48000.0
        self.interval = 10
        self.count = 0
    def get_sample(self):
        b = math.log(self.f_end / self.f_start) / self.interval
        a = 2 * math.pi * self.f_start / b
        t = self.interval * self.count / self.fs
        g_t = a * math.exp(b * t)
        self.count = self.count + 1
        return 3 * math.sin(g_t)

class Sweep:
    def __init__(self, freqct):
        self.freq = 1.0
        self.f_start = 1.0
        self.f_end = 10.0
        self.fs = 48000.0
        self.interval = 10.0
        self.count = 0
        self.freqct = freqct
    def log_sample(self):
        b = math.log(self.f_end / self.f_start) / self.interval
        a = 2 * math.pi * self.f_start / b
        t = self.interval * self.count / self.fs
        g_t = a * math.exp(b * t)
        self.count = self.count + 1
        return 3 * math.sin(g_t)
    def get_sample(self):
        self.f_start = self.f_end
        self.f_end = self.freqct.get_sample() * self.freq
        delta = self.count / self.fs
        delta = delta % 1.0
        t = self.interval * delta
        phase = 2 * math.pi * t * (self.f_start + (self.f_end - self.f_start) * delta / 2)
        self.count = (self.count + 1)
        return math.sin(phase)


# def sweep(f_start, f_end, interval, n_steps):
#     for i in range(n_steps):
#         delta = i / float(n_steps)
#         t = interval * delta
#         phase = 2 * pi * t * (f_start + (f_end - f_start) * delta / 2)
#         print t, phase * 180 / pi, 3 * sin(phase)

# sweep(1, 10, 5, 1000)

# graph_node(VCO(freq=10.0), 48000)
# graph_node(Saw(freq=1.0), 48000)
# graph_node(VCO(freq=5.0, freqct=Saw(freq=100.0)), 48000 * 3)

# graph_node(Sine(freq=10.0, fmct=[Saw(freq=3.0)]), 48000)
# graph_node(Saw(freq=1.0, gain=1.0, offset=1.0), 48000 * 3)
# graph_node(Sine(freq=1.0, fmct=[Saw(freq=1.0, gain=0.5, offset=0.5)]), 48000 * 3)

# graph_node(Saw(freq=10.0, fmct=[Saw(freq=1.0)]), 48000 * 2)

# graph_node(Sine(freq=10.0), 48000 * 2)
# graph_node(Sweep(freqct=Sine(freq=1.0)), 48000 * 2)

# graph_node(Saw(freq=2.4, gain=10.0), 48000)
# graph_node(LinToExp(Saw(freq=2.4, gain=1.0), 10.0), 48000)
# graph_node(Atten(LinToLog(Saw(freq=2.4, gain=1.0), 10.0), gain=20.0, offset=-10.0), 48000)
# graph_node(Sine(freq=50.0, fmct=[Atten(LinToExp(Saw(freq=2.4, gain=1.0), 10.0), gain=20.0, offset=-10.0)]), 48000)

# graph_node(Sine(freq=50.0, gainct=LinToExp(Saw(freq=0.5, gain=-1.0), 10.0), fmct=[Atten(LinToExp(Saw(freq=0.5, gain=-1.0), 1000.0), gain=50.0, offset=-10.0)]), 48000 * 2)

# NOTE: value at sample n = sin(2 * pi * (n / fs) * f(in Hz))
# NOTE: phase at sample n = 2 * pi * (n / fs) * f(in Hz)


# record_file(integrator, 3)

# vari = Mult(Random(100000))
#
# # graph_node(vari, 48000 * 10)
#
# kick = Sine(freq=100.0, gainct=LinToExp(Saw(freq=0.4, gain=-1.0, fmct=[Atten(vari, gain=10.0, offset = 100.0)]), 10.0), fmct=[Atten(LinToExp(Saw(freq=0.4, gain=-1.0, fmct=[Atten(vari, gain=10.0, offset = 100.0)]), 1000.0), gain=30.0, offset=-10.0)])
# #
# dly = Delay(Filter(kick, 0.02), 10000, 0.9)
#
# tp = GlobalTransport([Filter(dly, 0.02)])
# tp.start()

tp = GlobalTransport([
    Saw(freq=79.0, fmct=[
        Sine(freq=10.0, gain=100.0)
    ])
])

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
