import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from py_modular.time.transport import GlobalTransport
from py_modular.sound.oscillators import Tri, Random
from py_modular.effects.mixer import Atten
from py_modular.time.events import TriggerEvent
from py_modular.time.envelopes import ExpEnv
from py_modular.time.transport import EventSequencer

pitch_variation = Random(freq=0.76, gain=50.0, offset=100.0)
pitch_envelope = ExpEnv(1.0, gain=10.0, curve_gain=0.8)
gain_envelope = ExpEnv(1.0, curve_gain=0.92)

trigger = TriggerEvent([pitch_envelope, gain_envelope])
sequencer = EventSequencer([trigger], sequence=[48000, 60000, 47000])

ping_sound = Tri(freq=250.0, gain=0.75, gainct=gain_envelope, fmct=[pitch_envelope, pitch_variation])

global_transport = GlobalTransport([sequencer], input_device=15, output_device=15)
global_transport.chs[0].add_node(ping_sound)
global_transport.chs[1].add_node(ping_sound)

global_transport.start()
