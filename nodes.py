from time import sleep
import struct
import math
import random

from debug_utils import *
from osc_nodes import *
from mixer_nodes import *
from transport_nodes import *
from event_nodes import *

BUFFER_SIZE = 2048
TEST_FILE = []

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
    def get_sample(self, time):
        samp = (self.node.get_sample(time) + self.buffer[self.txrx] * self.fb) / 1.5
        value = self.buffer[self.txrx]
        self.buffer[self.txrx] = samp
        self.txrx = (self.txrx + 1) % self.len
        return value

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

mo = Sine(125.0)
no = Saw(400.0)
pe = PitchEvent([mo, no], 100000)

eh = EventHandler([pe])
nh = NodeHandler([Mixer([no, mo], gainct=Random(freq=1, gain=0.8))])
rev = NodeHandler([Delay(Mixer([no, mo], gainct=Random(1)), 10000, 1.2)])

GlobalTransport([nh, rev], [eh]).start()

# record_file(Random(2000, gainct=Atten(LinToExp(Saw(freq=1.0, gain=-1.0), curve_gain=0.93), gain=0.5, offset=0.5)), seconds=10)

# GlobalTransport([
#     Delay(Random(2000, gainct=Atten(LinToExp(Saw(freq=1.0, gain=-1.0), curve_gain=0.93), gain=0.5, offset=0.5)), 3000, 1.2)
# ]).start()

# node = Saw(freq=4.0)
# node = LinToExp(Saw(freq=15.0, gain=-1.0), curve_gain=1.0)
#
# graph_node_lin(node, 48000)
# graph_node(Square(freq=20, pwmct=Saw(freq=1)), 48000)
# GlobalTransport([Square(freq=240, pwmct=Sine(freq=1, fmct=[Random(freq=0.26, gain=20.0)]))]).start()
