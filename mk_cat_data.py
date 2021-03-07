import csv
import pandas as pd
from sys import exit
import random

from debug_utils import *
from osc_nodes_c import *
from mixer_nodes import *
from transport_nodes import *
from event_nodes import *
from env_nodes import *
from processing_nodes import *
from dsp_nodes import *
from synth_models import *

# test_blocks = []
# train_blocks = []
# test_freqs = []
# train_freqs = []
# test_types = []
# train_types = []
# bias = 0

x_train = []
y_train = []
x_test = []
y_test = []

def make_block():
    f = random.random() * 5000 + 50
    t = int(random.random() * 4)
    node = None
    if t == 0:
        node = Sine(freq=f)
    elif t == 1:
        node = Saw(freq=f)
    elif t == 2:
        node = Square(freq=f)
    elif t == 3:
        node = Tri(freq=f)
    tp = GlobalTransport([], 1)
    tp.chs[0].add_node(node)
    tp.get_block()
    data = tp.block
    return [samp[0] for samp in data]

def make_test_item():
    f = random.random() * 5000 + 50
    t = int(random.random() * 4)
    node = None
    if t == 0:
        node = Sine(freq=f)
    elif t == 1:
        node = Saw(freq=f)
    elif t == 2:
        node = Square(freq=f)
    elif t == 3:
        node = Tri(freq=f)
    tp = GlobalTransport([], 1)
    tp.chs[0].add_node(node)
    tp.get_block()
    data = tp.block
    samps = [samp[0] for samp in data]
    x_train.append(samps)

def make_train_item():
    f = random.random() * 5000 + 50
    t = int(random.random() * 4)
    node = None
    if t == 0:
        node = Sine(freq=f)
    elif t == 1:
        node = Saw(freq=f)
    elif t == 2:
        node = Square(freq=f)
    elif t == 3:
        node = Tri(freq=f)
    tp = GlobalTransport([], 1)
    tp.chs[0].add_node(node)
    tp.get_block()
    data = tp.block
    samps = [samp[0] for samp in data]
    train_blocks.append(samps)
    train_types.append(t)

for i in range(10000):
    make_train_item()
    print(str(i * 100.0 / 10000.0) + "% done")

for i in range(1000):
    make_test_item()
    print(str(i * 100.0 / 1000.0) + "% done")

x_train = pd.DataFrame(train_blocks)
y_train = pd.DataFrame(train_types)

x_test = pd.DataFrame(test_blocks)
y_test = pd.DataFrame(test_types)

x_train.to_csv('~/PycharmProjects/tf_project/x_train.csv', index=False, header=False)
y_train.to_csv('~/PycharmProjects/tf_project/y_train.csv', index=False, header=False)

x_test.to_csv('~/PycharmProjects/tf_project/x_test.csv', index=False, header=False)
y_test.to_csv('~/PycharmProjects/tf_project/y_test.csv', index=False, header=False)
