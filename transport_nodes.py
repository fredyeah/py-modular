import threading
import sounddevice as sd
import numpy as np

class GlobalTransport:
    def __init__(self, node_handlers, event_handlers, buffer_len=1024, fs=48000.0):
        self.buffer_len = buffer_len
        self.node_handlers = node_handlers
        self.event_handlers = event_handlers
        self.count = 0;
        self.buffer = []
        self.fs = fs
    def add_node(self, node):
        self.nodes.append(node)
    def get_block(self):
        self.buffer = [[],[]]
        oc = self.count
        for i in range(2):
            self.count = oc
            for s in range(int(self.buffer_len)):
                sample = 0
                for handler in self.node_handlers[i]:
                    sample = handler.sample_callback(self.count) + sample
                try:
                    sample = sample / len(self.node_handlers[i])
                except:
                    pass
                for handler in self.event_handlers[i]:
                    handler.sample_callback(self.count)
                self.buffer[i].append(sample)
                self.count = self.count + 1
        return self.buffer
    def buffer_cb(self, indata, outdata, frames, time, status):
        block = self.get_block()
        ch_num = 2
        for ch in range(ch_num):
            chan = np.array(block[ch]).reshape(self.buffer_len)
            outdata[:, ch] = chan
    def begin_thread(self):
        while True:
            with sd.Stream(channels=2, samplerate=48000, blocksize=self.buffer_len, callback=self.buffer_cb):
                sd.sleep(1000 * 60 * 60 * 24)
    def start(self):
        threading.Thread(target=self.begin_thread).start()

class NodeHandler:
    def __init__(self, nodes, fs=48000.0):
        self.nodes = nodes
        self.fs = fs
    def sample_callback(self, sample):
        t = sample / self.fs
        sample_value = 0.0
        for node in self.nodes:
            sample_value = node.get_sample(t) + sample_value
        sample_value = sample_value / len(self.nodes)
        return sample_value

class EventHandler:
    def __init__(self, events, fs=48000.0):
        self.events = events
        self.fs = fs
    def sample_callback(self, sample):
        t = sample / self.fs
        for event in self.events:
            if sample % event.sample_freq == 0:
                event.get_event(t)

class EventSequencer:
    def __init__(self, events, fs=48000.0, sequence=[]):
        self.events = events
        self.fs = fs
        self.count = 0
        self.pos = 0
        self.sequence = sequence
    def sample_callback(self, sample):
        t = sample / self.fs
        if self.count == self.sequence[self.pos]:
            self.pos = self.pos + 1
            self.pos = self.pos % len(self.sequence)
            self.count = 0
            for event in self.events:
                event.get_event(t)
        self.count = self.count + 1
