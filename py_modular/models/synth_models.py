import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from sound_nodes.osc_nodes import *

class FMSynth:
    def __init__(self):
        self.op1 = Sine()
        self.op2 = Sine(fmct=[self.op1])
        self.op3 = Sine(fmct=[self.op2])
    def get_sample(self, time):
        return self.op3.get_sample(time)
