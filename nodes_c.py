

from debug_utils import *
from osc_nodes_c import *
from mixer_nodes import *
from transport_nodes import *
from event_nodes import *
from env_nodes import *
from processing_nodes import *
from dsp_nodes import *
from synth_models import *

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

t = Sine(freq=200, fmct=[Random(1, gain=100.0)])
md = MultiChannelDelay([t], [1000, 2000], 1.2)

tp = GlobalTransport([], 2)

tp.chs[0].add_node(t)
# tp.chs[0].add_node(md)
# tp.chs[1].add_node(md)
# tp.chs[2].add_node(fm)
# tp.chs[0].add_node(kick)
tp.chs[1].add_node(t)
# tp.chs[2].add_node(t)
# tp.chs[3].add_node(t)
# tp.chs[4].add_node(t)
# tp.chs[1].add_node(t)
# tp.chs[1].add_node(t)
# tp.chs[1].add_node(t)
# tp.chs[1].add_node(kick)

# tp.start()

iter = [9.0] * 1024 * 2;

t = time.perf_counter()
for s in range(tp.buffer_len):
    sample = []
    for ch in tp.chs:
        # x = time.perf_counter()
        sample.append(ch.sample_callback(tp.count))
        # print(time.perf_counter() - x)
    for handler in tp.event_handlers:
        handler.sample_callback(tp.count)
    tp.count = tp.count + 1
print(time.perf_counter() - t)


cnt = 0
for ch in tp.chs:
    cnt = cnt + 1
    sample.append(ch.sample_callback(tp.count))
print(cnt)
cnt = 0
for handler in tp.event_handlers:
    cnt = cnt + 1
    handler.sample_callback(tp.count)
print(cnt)

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
