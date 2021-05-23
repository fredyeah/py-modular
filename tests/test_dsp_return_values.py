from py_modular.effects.dsp import Delay, MultiTapDelay, MultiChannelDelay
from py_modular.sound.oscillators import Sine
import pytest
from random import random

@pytest.fixture
def s():
    return Sine()

def test_delay_return(s):
    d = Delay([s], 1000, 1.0)
    v = d.get_sample(random())
    assert isinstance(v, float)

def test_multi_tap_delay_return(s):
    d = MultiTapDelay(s, [1000, 2000, 3000])
    v = d.get_sample(random())
    assert isinstance(v, float)

def test_multi_channel_delay_return(s):
    d = MultiChannelDelay([s], [1000, 2000], 1.0)
    t = random()
    v_a = d.get_sample(t)
    v_b = d.get_sample(t)
    assert isinstance(v_a, float)
    assert isinstance(v_b, float)
