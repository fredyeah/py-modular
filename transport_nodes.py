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
        self.buffer = []
        for i in range(self.buffer_len):
            sample = 0
            for handler in self.node_handlers:
                sample = handler.sample_callback(self.count) + sample
            sample = sample / len(self.node_handlers)
            for handler in self.event_handlers:
                handler.sample_callback(self.count)
            self.buffer.append(sample)
            self.count = self.count + 1
        return self.buffer
    def buffer_cb(self, indata, outdata, frames, time, status):
        block = self.get_block()
        arry = np.array(block).reshape((self.buffer_len, 1))
        outdata[:] = arry
    def begin_thread(self):
        while True:
            with sd.Stream(channels=1, samplerate=48000, blocksize=self.buffer_len, callback=self.buffer_cb):
                sd.sleep(int((48000 / self.buffer_len) * 1000))
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
        for event in self.events:
            if sample % event.sample_freq == 0:
                event.get_event()
