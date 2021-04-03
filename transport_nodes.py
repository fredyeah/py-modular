import threading
import sounddevice as sd
import numpy as np
import time

class NodeHandler:
    def __init__(self, nodes=[], fs=48000.0):
        self.nodes = nodes
        self.fs = fs
    def add_node(self, node):
        self.nodes.append(node)
    def sample_callback(self, sample):
        t = sample / self.fs
        sample_value = 0.0
        for node in self.nodes:
            sample_value = node.get_sample(t) + sample_value
        if len(self.nodes) > 0:
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

class GlobalTransport:
    def __init__(self, event_handlers, channels=2, buffer_len=1024, fs=48000.0):
        # sd.default.device = [3, 3]
        # print("default device is: ", sd.default.device)
        self.buffer_len = buffer_len
        self.event_handlers = event_handlers
        self.count = 0;
        self.block = []
        self.next_block = []
        for i in range(self.buffer_len):
            self.block.append([0.0] * channels)
            self.next_block.append([0.0] * channels)
        self.channels = channels
        self.chs = []
        for i in range(channels):
            self.chs.append(NodeHandler([]))
        self.fs = fs
        self.need_block = False
    def add_node(self, node):
        self.nodes.append(node)
    def get_block(self):
        # t = time.perf_counter()
        self.block = []
        for s in range(self.buffer_len):
            sample = []
            for ch in self.chs:
                sample.append(ch.sample_callback(self.count))
            for handler in self.event_handlers:
                handler.sample_callback(self.count)
            self.count = self.count + 1
            self.block.append(sample)
        # print(time.perf_counter() - t)
    def buffer_cb(self, indata, outdata, frames, timer, status):
        # print(status)
        outdata[:] = self.block
        self.get_block()
        # self.need_block = True
    def block_listen(self):
        while True:
            if self.need_block == True:
                self.get_block()
                self.need_block = False
    def begin_thread(self):
        while True:
            with sd.Stream(channels=self.channels, samplerate=48000, blocksize=self.buffer_len, callback=self.buffer_cb):
                sd.sleep(1000 * 60 * 60 * 24)
    def start(self):
        threading.Thread(target=self.begin_thread).start()
        # threading.Thread(target=self.block_listen).start()
