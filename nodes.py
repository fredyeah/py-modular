from util_nodes.debug_utils import *
from sound_nodes.osc_nodes import *
from sound_nodes.granular_nodes import *
from effect_nodes.mixer_nodes import *
from time_nodes.transport_nodes import *
from time_nodes.event_nodes import *
from time_nodes.env_nodes import *
from effect_nodes.processing_nodes import *
from effect_nodes.dsp_nodes import *
from models.synth_models import *
import numpy as np
from sys import exit
import matplotlib.pyplot as plt

sq = Square(1.0)
sw = Sine(0.4)
sn = Sine(200.0)
lim = Lim(sq)


#
# fm2 = Sine(freq=300, fmct=[Sine(freq=200, fmct=[Sine(freq=570)])])
#
# s = Sine(freq=300, fmct=[Sine(freq=200)])
#
# # graph_node_lin(s, 48000)
#
# pn = Panner(fm, posct=sn)
#


# d = MultiTapDelay(t, taps=[
# 400, 5000, 300, 1000, 20000
# ])

# lchd = Delay([t], 1000, 1.2)
# rchd = Delay([t], 2000, 1.1)
#
# lchd.add_input(rchd)
# rchd.add_input(lchd)

kick = Sine(freq=60, gainct=Atten(LinToExp(Saw(freq=1, gain=-1.0), 0.8), gain=0.5, offset=0.5), fmct=[
    Atten(LinToExp(Saw(freq=1, gain=-1.0), 0.9), gain=10, offset=10)
])

# graph_node_lin(LinToExp(Saw(freq=1)), 48000)

fm = FMSynth()
fm.op1.freq = 570.0
fm.op2.freq = 209.3
fm.op1.gain = 190.0
fm.op2.gain = 30.35
fm.op3.freq = 300.0
fm.op3.gainct = Saw(0.4)

grains = np.load('clouds/debussy_embeddings_interpolated.npy')
grains = window_grains_tri(grains)
gran = GranBase(grains)

# plt.plot(grains[0])
# plt.show()
# grains = window_grains(grains)
# plt.plot(grains[0])
# plt.show()
# exit()

t = Sine(freq=200, fmct=[Random(1, gain=100.0)])
md = MultiChannelDelay([gran], [1000, 2000], 1.2)

tp = GlobalTransport([], 2, fs=16000.0)

# TODO: should have three granulation types,
# slice before generating embeddings
# slice after generating embeddings
# interpolate between two embeddings





# tp.chs[0].add_node(t)
# tp.chs[1].add_node(t)
# tp.chs[0].add_node(md)
# tp.chs[1].add_node(md)
# tp.chs[0].add_node(gran)
# tp.chs[1].add_node(gran)
tp.chs[0].add_node(md)
tp.chs[1].add_node(md)
# tp.chs[0].add_node(md)
# tp.chs[1].add_node(md)
# tp.chs[2].add_node(fm)
# tp.chs[0].add_node(kick)
# tp.chs[1].add_node(t)
# tp.chs[2].add_node(t)
# tp.chs[3].add_node(t)
# tp.chs[4].add_node(t)
# tp.chs[1].add_node(t)
# tp.chs[1].add_node(t)
# tp.chs[1].add_node(t)
# tp.chs[1].add_node(kick)

tp.start()

# record_transport(tp, seconds=5.0)

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
