from random import random
from py_modular.sound.oscillators import Sine, Tri, Saw, Square, Random

def test_sine_return():
    s = Sine()
    r = random()
    v = s.get_sample(r)
    assert isinstance(v, float)

def test_tri_return():
    t = Tri()
    r = random()
    v = t.get_sample(r)
    assert isinstance(v, float)

def test_saw_return():
    s = Saw()
    r = random()
    v = s.get_sample(r)
    assert isinstance(v, float)

def test_square_return():
    s = Square()
    r = random()
    v = s.get_sample(r)
    assert isinstance(v, float)

def test_random_return():
    r = Random()
    ra = random()
    v = r.get_sample(ra)
    assert isinstance(v, float)
