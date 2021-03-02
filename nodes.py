

from debug_utils import *
from osc_nodes import *
from mixer_nodes import *
from transport_nodes import *
from event_nodes import *
from env_nodes import *
from processing_nodes import *
from dsp_nodes import *

sq = Square(120.0)
sw = Saw(120.0)
sn = Sine(200.0)
lim = Lim(sq)
GlobalTransport([
    [NodeHandler([lim])],
    [NodeHandler([sn])]
], [
    [],
    []
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
