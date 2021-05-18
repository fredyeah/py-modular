import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))

from py_modular.sound.granular import GranBase
from py_modular.sound.oscillators import Sine
from py_modular.effects.dsp import Delay
from py_modular.time.transport import GlobalTransport
from py_modular.utils.processing import window_grains_sin
import numpy as np

grains = np.load('generated_grain_cloud.npy')
windowed_grains = window_grains_sin(grains)

granulator = GranBase(windowed_grains, freq=5.0, jitter=3)

delay = Delay([granulator], 43000, 0.7)
delay = Delay([delay], 40000, 0.7)
delay = Delay([delay], 30000, 0.7)
delay = Delay([delay], 20000, 0.7)

delay_a = Delay([granulator], 42900, 0.7)
delay_a = Delay([delay_a], 40000, 0.7)
delay_a = Delay([delay_a], 30000, 0.7)
delay_a = Delay([delay_a], 20000, 0.7)

global_transport = GlobalTransport([])
global_transport.chs[0].add_node(delay)
global_transport.chs[1].add_node(delay_a)
global_transport.start()
