import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from py_modular.time.transport import GlobalTransport
from py_modular.sound.oscillators import Tri, Random
from py_modular.effects.mixer import Atten
from py_modular.effects.dsp import MultiChannelDelay
from py_modular.time.events import TriggerEvent
from py_modular.time.envelopes import ExpEnv
from py_modular.time.transport import EventSequencer

from random import randint

def get_ping_sound():
    pitch_variation = Random(freq=0.76, gain=50.0, offset=100.0)
    pitch_envelope = ExpEnv(1.0, gain=10.0, curve_gain=0.8)
    gain_envelope = ExpEnv(1.0, curve_gain=0.92)
    trigger = TriggerEvent([pitch_envelope, gain_envelope])
    sequencer = EventSequencer([trigger], sequence=[randint(30000, 60000) for i in range(randint(2, 6))])
    ping_sound = Tri(freq=250.0, gain=0.75, gainct=gain_envelope, fmct=[pitch_envelope, pitch_variation])
    return ping_sound, sequencer

num_pings = 2
event_handlers = []
sounds = []

for i in range(num_pings):
    sound, sequencer = get_ping_sound()
    event_handlers.append(sequencer)
    sounds.append(sound)

delay = MultiChannelDelay(sounds, [8477, 30298], 1.32)

global_transport = GlobalTransport(event_handlers, input_device=15, output_device=15)
global_transport.chs[0].add_node(delay)
global_transport.chs[1].add_node(delay)

global_transport.start()
