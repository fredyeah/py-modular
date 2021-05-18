from math import floor

class Delay:
    """
    :param nodes: An array of nodes that should be delayed
    :param len: The length of the delay line in samples
    :type len: int
    :param fb: The ammount of feedback into the delay line
    :type fb: float
    :ivar buffer: A buffer which contains audio data from the nodes
    :vartype buffer: array
    :ivar txrx: A pointer to the read/write position in the buffer
    :vartype txrx: int
    """
    def __init__(self, nodes, len, fb, lenct=None):
        self.nodes = nodes
        self.len = len
        self.buffer = [0.0] * len
        self.txrx = 0
        self.fb = fb
        self.lenct = lenct
    def add_input(self, node):
        """
        :param node: Node to add to the delay line
        """
        self.nodes.append(node)
    def get_sample(self, time):
        """
        :param time: The time in seconds of which the sample should be gotten
        :type time: float
        :returns: A PCM value for the node at the given time
        :rtype: float
        """
        if not self.lenct == None:
            self.len = floor(abs(self.lenct.get_sample(time)))
        samp = 0.0
        for node in self.nodes:
            samp = node.get_sample(time) + samp
        samp = samp / len(self.nodes)
        samp = (samp + self.buffer[self.txrx] * self.fb) / 1.5
        value = self.buffer[self.txrx]
        self.buffer[self.txrx] = samp
        self.txrx = (self.txrx + 1) % self.len
        return value

class MultiTapDelay:
    """
    :param node: The node which should be delayed
    :param taps: An array of positions where the delay line should be tapped
    :type taps: array(int)
    """
    def __init__(self, node, taps=[]):
        self.node = node
        self.taps = taps
        self.buffer = [0] * 48000
        self.count = 0
    def get_sample(self, time):
        """
        :param time: The time in seconds of which the sample should be gotten
        :type time: float
        :returns: A PCM value for the node at the given time
        :rtype: float
        """
        self.buffer[self.count] = self.node.get_sample(time)
        samp = 0.0
        for i in range(len(self.taps)):
            samp = samp + self.buffer[self.taps[i]]
            self.taps[i] = (self.taps[i] + 1) % len(self.buffer)
        samp = samp / len(self.taps)
        self.buffer[self.count] = (self.node.get_sample(time) + samp * 1.4) / 1.5
        self.count = (self.count + 1) % len(self.buffer)
        return (self.node.get_sample(time) + samp * 1.4) / 1.5

class MultiChannelDelay:
    """
    :param nodes: An array of nodes that should be fed into the delay line
    :param len: An array of lengths for each delay channel
    :type len: array(int)
    :param fb: Ammount of feedback into the delay line
    :type fb: float
    :ivar buffer: An array of buffers of audio data in the delay line
    :vartype buffer: array
    :ivar txrx: An array of read/write position values for the respective delay buffers
    :vartype txrx: array
    :ivar ch_num: The current channel number which the buffer will be read from
    :vartype ch_num: int
    """
    def __init__(self, nodes, len, fb):
        self.nodes = nodes
        self.len = [
            len[0],
            len[1]
        ]
        self.buffer = [
            [0.0] * len[0],
            [0.0] * len[1]
        ]
        self.txrx = [0, 0]
        self.fb = fb
        self.ch_num = 0
    def add_input(self, node):
        """
        :param node: Node to add to the delay line
        """
        self.nodes.append(node)
    def get_sample(self, time):
        """
        :param time: The time in seconds of which the sample should be gotten
        :type time: float
        :returns: A PCM value for the node at the given time
        :rtype: float
        """
        samp = 0.0
        for node in self.nodes:
            samp = node.get_sample(time) + samp
        samp = samp / len(self.nodes)
        c_n = self.ch_num
        samp = (samp + self.buffer[c_n][self.txrx[c_n]] * self.fb) / 1.5
        value = self.buffer[c_n][self.txrx[c_n]]
        self.buffer[c_n][self.txrx[c_n]] = samp
        self.txrx[c_n] = (self.txrx[c_n] + 1) % self.len[c_n]
        self.ch_num = (self.ch_num + 1) % len(self.buffer)
        return value
