import threading
import sounddevice as sd
import numpy as np

class GlobalTransport:
    def __init__(self, nodes, buffer_len=1024, fs=48000.0):
        self.buffer_len = buffer_len
        self.nodes = nodes
        self.count = 0;
        self.buffer = []
        self.fs = fs
    def add_node(self, node):
        self.nodes.append(node)
    def get_block(self):
        self.buffer = []
        for i in range(self.buffer_len):
            sample = 0
            for node in self.nodes:
                s = node.get_sample(self.count / self.fs)
                sample = (s + sample) / 2
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
