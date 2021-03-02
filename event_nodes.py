import random

class Event:
    def __init__(self, nodes=None, sample_freq=48000, fs=48000):
        self.nodes = nodes
        self.sample_freq = sample_freq
        self.fs = fs
    def get_event(self):
        for node in self.nodes:
            self.event_callback(node)
        return 0.0

class PitchEvent(Event):
    def event_callback(self, node):
        node.freq = (random.random() * 100 + 200)
