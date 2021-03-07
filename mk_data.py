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

test_blocks = []
train_blocks = []
test_freqs = []
train_freqs = []
bias = 1000

for i in range(1000):
    sine = Sine(freq=i+bias)
    tp = GlobalTransport([], 1)
    tp.chs[0].add_node(sine)
    tp.get_block()
    data = tp.block
    freq = float(i+bias)
    samps = [samp[0] for samp in data]
    train_blocks.append(samps)
    train_freqs.append(freq)

for i in range(100):
    f = random.random() * 1000 + 1000
    sine = Sine(freq=f)
    tp = GlobalTransport([], 1)
    tp.chs[0].add_node(sine)
    tp.get_block()
    data = tp.block
    freq = float(f)
    samps = [samp[0] for samp in data]
    test_blocks.append(samps)
    test_freqs.append(freq)

x_train = pd.DataFrame(train_blocks)
y_train = pd.DataFrame(train_freqs)

x_test = pd.DataFrame(test_blocks)
y_test = pd.DataFrame(test_freqs)

x_train.to_csv('~/PycharmProjects/tf_project/x_train.csv', index=False, header=False)
y_train.to_csv('~/PycharmProjects/tf_project/y_train.csv', index=False, header=False)

x_test.to_csv('~/PycharmProjects/tf_project/x_test.csv', index=False, header=False)
y_test.to_csv('~/PycharmProjects/tf_project/y_test.csv', index=False, header=False)
