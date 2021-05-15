import random

class Event:
    def __init__(self, nodes=None, sample_freq=48000, fs=48000):
        self.nodes = nodes
        self.sample_freq = sample_freq
        self.fs = fs
    def get_event(self, time):
        for node in self.nodes:
            self.event_callback(node, time)
        return 0.0

class PitchEvent(Event):
    def event_callback(self, node, time):
        node.freq = (random.random() * 100 + 120)

class TriggerEvent(Event):
    def event_callback(self, node, time):
        node.trigger(time)
