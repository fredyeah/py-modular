from time import sleep
import struct
import math
import random

from debug_utils import *
from osc_nodes import *
from mixer_nodes import *
from transport_nodes import *

BUFFER_SIZE = 2048
TEST_FILE = []

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
        val = (10 * math.log10(val+0.0) + 60.0) / 60.0
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

# graph_node(Square(freq=20, pwmct=Saw(freq=1)), 48000)
GlobalTransport([Square(freq=240, pwmct=Sine(freq=1, fmct=[Random(freq=0.26, gain=20.0)]))]).start()
