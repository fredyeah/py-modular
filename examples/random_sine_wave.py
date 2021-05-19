import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from py_modular.sound.oscillators import Sine, Random
from py_modular.time.transport import GlobalTransport

random_oscillator = Random(freq=1.1, gain=50.0, offset=0.5)
sine_oscillator = Sine(gain=0.85, fmct=[random_oscillator])

global_transport = GlobalTransport([], input_device=15, output_device=15)
global_transport.chs[0].add_node(sine_oscillator)
global_transport.chs[1].add_node(sine_oscillator)

global_transport.start()
