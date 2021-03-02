from time import sleep
import struct
import math
import random

from debug_utils import *
from osc_nodes import *
from mixer_nodes import *
from transport_nodes import *
from event_nodes import *
from env_nodes import *
from processing_nodes import *

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

sq = Square(120.0)
sw = Saw(120.0)
sn = Sine(120.0)
lim = Lim(sq)
GlobalTransport([
    NodeHandler([lim])
], [

]).start()
# graph_node_lin(sq, 48000)
# graph_node_lin(lim, 48000)

# env = ExpEnv(len=1.3, curve_gain=0.8)
# amb = ExpEnv(len=0.8, curve_gain=0.5)
# mo = Sine(125.0, gainct=env)
# ctl = Sine(59, fmct=[Atten(amb, gain=10.0)])
#
# pe = PitchEvent([mo], 100000)
# te = TriggerEvent([env])
# slope = TriggerEvent([amb])
#
# ag = EventSequencer([slope], sequence=[
#     40000
# ])
# seq = EventSequencer([te], sequence=[48000])
# eh = EventHandler([te])
# nh = NodeHandler([Mixer([mo, ctl])])
#
# gt = GlobalTransport([nh], [seq, ag]).start()
