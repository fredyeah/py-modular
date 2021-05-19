import threading
import sounddevice as sd
import numpy as np

class NodeHandler:
    """
    :param nodes: An array of nodes that should be played
    :type nodes: array
    :param fs: sample frequency of the handler, used to calculate a value of time
    :type fs: float
    """
    def __init__(self, nodes=[], fs=48000.0):
        self.nodes = nodes
        self.fs = fs
    def add_node(self, node):
        """
        :param node: Node to add to the handler
        """
        self.nodes.append(node)
    def sample_callback(self, sample):
        """
        :param sample: The current sample that should be used to calculate any events or values
        :type sample: int
        :returns: A PCM value representing all the nodes in the node handler mixed together
        :rtype: float
        """
        t = sample / self.fs
        sample_value = 0.0
        for node in self.nodes:
            sample_value = node.get_sample(t) + sample_value
        if len(self.nodes) > 0:
            sample_value = sample_value / len(self.nodes)
        return sample_value

class EventHandler:
    """
    :param events: An array of events that should be handled
    :type events: array
    :param fs: sample frequency of the handler, used to calculate a value of time
    :type fs: float
    """
    def __init__(self, events, fs=48000.0):
        self.events = events
        self.fs = fs
    def sample_callback(self, sample):
        """
        :param sample: The current sample that should be used to calculate any events or values
        :type sample: in
        """
        t = sample / self.fs
        for event in self.events:
            if sample % event.sample_freq == 0:
                event.get_event(t)

class EventSequencer:
    """
    :param events: An array of events that should be handled
    :type events: array
    :param fs: sample frequency of the handler, used to calculate a value of time
    :type fs: float
    :param sequence: An array of sample values at which events should be fired
    :type sequence: array(int)
    """
    def __init__(self, events, fs=48000.0, sequence=[]):
        self.events = events
        self.fs = fs
        self.count = 0
        self.pos = 0
        self.sequence = sequence
    def sample_callback(self, sample):
        """
        :param sample: The current sample that should be used to calculate any events or values
        :type sample: int
        """
        t = sample / self.fs
        if self.count == self.sequence[self.pos]:
            self.pos = self.pos + 1
            self.pos = self.pos % len(self.sequence)
            self.count = 0
            for event in self.events:
                event.get_event(t)
        self.count = self.count + 1

class GlobalTransport:
    """
    :param event_handlers: An array of event handlers that should sync to this transport
    :type event_handlers: array
    :param input_device: The input device index. Can be found by running `python -m sounddevice` and selecting your desired device
    :type input_device: int
    :param output_device: The output device index. Can be found by running `python -m sounddevice` and selecting your desired device
    :type output_device: int
    :param channels: Number of channels the transport should have
    :type channels: int
    :param buffer_len: Audio buffer length of each channel
    :type buffer_len: int
    :param fs: Sampling frequency of the transport in Hz
    :type fs: float
    :ivar count: The current sample the transport is on
    :vartype count: int
    :ivar block: An array of audio data that will be output on the next buffer callback
    :vartype block: array
    :ivar chs: An array of node handlers that will be called for each channel
    """
    def __init__(self, event_handlers, input_device=0, output_device=0, channels=2, buffer_len=1024, fs=48000.0):
        sd.default.device = [input_device, output_device]
        print("default device is: ", sd.default.device)
        self.buffer_len = buffer_len
        self.event_handlers = event_handlers
        self.count = 0;
        self.block = []
        for i in range(self.buffer_len):
            self.block.append([0.0] * channels)
        self.channels = channels
        self.chs = []
        for i in range(channels):
            self.chs.append(NodeHandler([]))
        self.fs = fs
        self.need_block = False
    def get_block(self):
        """Executed every time an audio buffer is needed

        """
        self.block = []
        for s in range(self.buffer_len):
            sample = []
            for ch in self.chs:
                sample.append(ch.sample_callback(self.count))
            for handler in self.event_handlers:
                handler.sample_callback(self.count)
            self.count = self.count + 1
            self.block.append(sample)
    def buffer_cb(self, indata, outdata, frames, timer, status):
        outdata[:] = self.block
        self.get_block()
    def begin_thread(self):
        while True:
            with sd.Stream(channels=self.channels, samplerate=48000, blocksize=self.buffer_len, callback=self.buffer_cb):
                sd.sleep(1000 * 60 * 60 * 24)
    def start(self):
        threading.Thread(target=self.begin_thread).start()
