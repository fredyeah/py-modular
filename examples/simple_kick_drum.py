import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from py_modular.sound.oscillators import Sine, Saw
from py_modular.effects.mixer import Atten, LinToExp
from py_modular.time.transport import GlobalTransport

def create_envelope(freq, curve, gain, offset):
    envelope_base = Saw(freq=freq, gain=-1.0)
    curved_envelope = LinToExp(envelope_base, curve)
    offset_envelope = Atten(curved_envelope, gain=gain, offset=offset)
    return offset_envelope

gain_envelope = create_envelope(1, 0.8, 0.5, 0.5)
pitch_envelope = create_envelope(1, 0.9, 10, 10)

kick = Sine(freq=60, gainct=gain_envelope, fmct=[pitch_envelope])

global_transport = GlobalTransport([])
global_transport.chs[0].add_node(kick)
global_transport.chs[1].add_node(kick)

global_transport.start()
