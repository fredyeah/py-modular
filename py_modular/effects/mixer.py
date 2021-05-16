import math

class Mixer:
    """
    :param nodes: An array of nodes that should be mixed together. All nodes should have a `get_sample` method that, given a value of time, should return a PCM value
    :param gain: An ammount of gain, from 0.0 to 1.0 to apply to the output of the mixer
    :type gain: float
    :param gainct: A node, with a `get_sample` method that, given a value of time, should return a PCM value. The `get_sample` output value will control the gain of the mixer on a sample by sample basis
    """
    def __init__(self, nodes, gain=1.0, gainct=None):
        self.nodes = nodes
        self.gain = float(gain)
        self.gainct = gainct
    def get_sample(self, time):
        """
        :param time: The time in seconds of which the sample should be gotten
        :type time: float
        :returns: A PCM value for the node at the given time
        :rtype: float
        """
        sample = 0
        for node in self.nodes:
            sample = node.get_sample(time) + sample
        if not self.gainct == None:
            self.gain = self.gainct.get_sample(time)
        sample = sample / len(self.nodes)
        return sample * self.gain

class Atten:
    """
    :param node: The node that will be attenuated
    :param gain: The linear gain applied to the node
    :type gain: float
    """
    def __init__(self, node, gain=1.0, offset=0.0):
        self.node = node
        self.gain = gain
        self.offset = offset
    def get_sample(self, time):
        """
        :param time: The time in seconds of which the sample should be gotten
        :type time: float
        :returns: A PCM value for the node at the given time
        :rtype: float
        """
        return self.node.get_sample(time) * self.gain + self.offset

class LinToExp:
    """
    :param node: The node whos output should be transformed
    :param curve_gain: A value between -1.0 and 1.0 that determines the ammount of transform. -1.0 is logarithmic, 1.0 is exponential, and 0.0 is linear.
    :type curve_gain: float
    :param curvect: A node that will directly control `curve_gain`
    """
    def __init__(self, node, curve_gain=1.0, curvect=None):
        self.node = node
        value = curve_gain * 0.999999
        if value > 0.0:
            self.curve_gain = -1.0 / (value - 1.0)
        else:
            self.curve_gain = value + 1
        self.curvect = curvect
    def curve_gain_to(self, value):
        """
        :param value: A value between -1.0 and 1.0 that will control `curve_gain`
        :type value: float
        """
        value = value * 0.999999
        if value > 0.0:
            self.curve_gain = -1.0 / (value - 1.0)
        else:
            self.curve_gain = value + 1
    def get_sample(self, time):
        """
        :param time: The time in seconds of which the sample should be gotten
        :type time: float
        :returns: A PCM value for the node at the given time
        :rtype: float
        """
        if not self.curvect == None:
            self.curve_gain_to(self.curvect.get_sample(time))
        s = self.node.get_sample(time) * 0.5 + 0.5
        value = math.pow(s, self.curve_gain) - 0.5
        return value * 2.0

class Panner:
    """
    :param node: A node that will be panned
    :param pos: A value between 0.0 and 1.0 that determines the possition betwen left and right channels
    :type pos: float
    :param posct: A node that will control the position on a sample by sample basis
    :ivar lch: A node that will output the left channel
    :ivar rch: A node that will output the right channel 
    """
    def __init__(self, node, pos=1.0, posct=None):
        self.node = node
        self.pos = pos
        self.posct = posct
        self.lch = Atten(node, gain=self.pos)
        self.rch = Atten(node, gain=(1.0 - self.pos))
    def get_sample(self, time):
        """
        :param time: The time in seconds of which the sample should be gotten
        :type time: float
        :returns: A PCM value for the node at the given time
        :rtype: float
        """
        if not self.posct == None:
            self.pos = self.posct.get_sample(time) * 0.5 + 0.5
            self.lch.gain = self.pos
            self.rch.gain = 1.0 - self.pos
        return 0.0
