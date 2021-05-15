from debug_utils import *
from osc_nodes import *
from mixer_nodes import *
from transport_nodes import *
from event_nodes import *
from env_nodes import *
from processing_nodes import *
from dsp_nodes import *
from synth_models import *

osc = Square(freq=100, gainct=LinToExp(Atten(Saw(freq=0.3), gain=-0.5, offset=0.5), 0.5))
# osc = Saw(freq=100)

# delay = Delay()

graph_node_lin(osc, 48000)

gt = GlobalTransport([], 1)

gt.chs[0].add_node(osc)
# gt.chs[1].add_node(osc)

gt.start()
