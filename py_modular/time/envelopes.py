import math

class Envelope:
    """
    :param len: Length of the envelope in seconds
    :type len: float
    :ivar triggered: If the envelope is triggered or not
    :vartype triggered: boolean
    :ivar start_time: The start time in seconds of the last envelope cycle
    :vartype start_time: float
    """
    def __init__(self, len):
        self.len = float(len)
        self.triggered = False
        self.start_time = 0.0
    def trigger(self, time):
        """
        :param time: A time in seconds
        :type time: float
        """
        self.triggered = True
        self.start_time = time
    def get_sample(self, time):
        """
        :param time: The time in seconds of which the sample should be gotten
        :type time: float
        :returns: A PCM value for the node at the given time
        :rtype: float
        """
        t = time - self.start_time
        if t > (1.0 / self.len):
            self.triggered = False
        if self.triggered == True:
            phase = self.len * math.pi * t + 0.5 * math.pi
            return math.atan(math.tan(phase)) * -1.0 / math.pi + 0.5
        else:
            return 0.0

class ExpEnv(Envelope):
    """
    :param curve_gain: A value between -1.0 and 1.0 that determines the ammount of transform. -1.0 is logarithmic, 1.0 is exponential, and 0.0 is linear.
    :type curve_gain: float
    :param curvect: A node that will directly control `curve_gain`
    :param roll_off: A value that will control the ammount of filtering on sharp edges of the waveform
    :type roll_off: float
    """
    def __init__(self, len, gain=1.0, curve_gain=1.0, curvect=None, roll_off=100.0):
        super().__init__(len)
        self.gain = float(gain)
        self.roll_off = roll_off
        self.curvect = curvect
        value = curve_gain * 0.999999
        self.last_value = 0.0
        if value > 0.0:
            self.curve_gain = -1.0 / (value - 1.0)
        else:
            self.curve_gain = value + 1
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
        t = time - self.start_time
        if t > (1.0 / self.len):
            self.triggered = False
            if not self.curvect == None:
                self.curve_gain_to(self.curvect.get_sample(time))
        if self.triggered == True:
            phase = self.len * math.pi * t + 0.5 * math.pi
            s = math.atan(math.tan(phase)) * -1.0 / math.pi + 0.5
            value = math.pow(s, self.curve_gain)
            self.last_value = (value + self.roll_off * self.last_value) / (self.roll_off + 1)
            return self.last_value * self.gain
        else:
            return 0.0
