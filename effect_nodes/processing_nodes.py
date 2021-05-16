import math

class Filter:
    """
    :param node: The node whos output should be filtered
    :param coef: The filter coefficient
    :type coef: float
    """
    def __init__(self, node, coef=0.0):
        self.node = node
        self.coef = coef
        self.out_data = 0.0
    def get_sample(self, time):
        """
        :param time: The time in seconds of which the sample should be gotten
        :type time: float
        :returns: A PCM value for the node at the given time
        :rtype: float
        """
        in_data = self.node.get_sample(time)
        self.out_data = self.out_data - (self.coef * (self.out_data - in_data))
        return self.out_data

class Lim:
    """
    :param node: The node whos output should be limited
    :param roll_off: The intensity of the limiter
    :type roll_off: float 
    """
    def __init__(self, node, roll_off=100.0):
        self.node = node
        self.last_value = 0.0
        self.roll_off = roll_off
    def get_sample(self, time):
        """
        :param time: The time in seconds of which the sample should be gotten
        :type time: float
        :returns: A PCM value for the node at the given time
        :rtype: float
        """
        s = self.node.get_sample(time)
        self.last_value = (s + self.roll_off * self.last_value) / (self.roll_off + 1)
        value = math.atan(self.last_value * 3.0) * 2.0 / math.pi
        return value
