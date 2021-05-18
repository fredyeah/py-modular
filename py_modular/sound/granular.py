from random import random
from math import floor
random.__module__ = 'random'

class GranBase:
    """
    :param grains: An array of audio buffers that will be used as a grain cloud
    :type grains: array(array)
    :param freq: Frequency in Hz that grains will be fired at
    :type freq: float
    :param jitter: Ammount of jitter to apply to the grain firing frequency
    :type jitter: float
    :param random_offset: An ammount of randomness that determines the sequence in which grains are fired
    :type random_offset: int
    :param gain: An ammount of gain to apply to the output
    :type gain: float
    :param offset: An ammount of offset to apply to the output
    :type offset: float
    :ivar freq_in_seconds: The frequency represented as an ammount of time in seconds
    :vartype freq_in_seconds: float
    :ivar current_grain: The index of the currently playing grain
    :vartype current_grain: int
    :ivar playing_grains: An array of grain indecies that correspond to the grains currently playing
    :vartype playing_grains: array
    :ivar grain_positions: An array of indecies that correspond to the playback posistion of each grain
    :vartype grain_positions: array(array)
    :ivar time: The last value of time recieved
    :vartype time: float
    :ivar increment: The number of grains to increment every time a grain is fired.
    :vartype increment: int
    """
    def __init__(self, grains, freq=10.0, jitter=0, random_offset=0, gain=1.0, offset=0.0):
        self.grains = grains
        self.num_grains = len(grains)
        self.current_grain = 0
        self.playing_grains = [0]
        self.grain_positions = [0] * self.num_grains
        self.freq = float(freq)
        self.freq_in_seconds = 1.0 / self.freq
        self.jitter = float(jitter)
        self.random = random_offset
        self.time = 0.0
        self.gain = float(gain)
        self.offset = float(offset)
        self.increment = 1
    def gain_to(self, gain):
        """
        :param gain: A value to change the gain to
        :type gain: float
        """
        self.gain = float(gain)
    def make_jitter(self):
        """A function that invokes an ammount of jitter on the grain firing frequency

        """
        self.freq_in_seconds = 1.0 / (self.freq + (random() - 0.5) * self.jitter)
    def fire_grain(self):
        """A function that fires a grain and increments pointers accordingly

        """
        self.current_grain = (self.current_grain + self.increment + floor(random() * self.random * self.increment)) % self.num_grains
        if self.current_grain >= self.num_grains - 1:
            self.increment = -1
        if self.current_grain <= 0:
            self.increment = 1
        self.playing_grains.append(self.current_grain)
        self.make_jitter()
    def get_pcm_value(self, time):
        """
        :param time: The time in seconds of which the PCM value should be gotten for
        :type time: float
        :returns: A PCM value for the granulator at a given time
        :rtype: float
        """
        values = []
        for grain in self.playing_grains:
            self.grain_positions[grain] = self.grain_positions[grain] + 1
            if(self.grain_positions[grain] >= len(self.grains[grain])):
                self.playing_grains.remove(grain)
                self.grain_positions[grain] = 0
            values.append(self.grains[grain][self.grain_positions[grain]])
        if(len(values) > 0):
            return sum(values) / len(values)
        return 0.0
    def get_sample(self, time):
        """
        :param time: The time in seconds of which the sample should be gotten
        :type time: float
        :returns: A PCM value for the granulator at a given time that has been adjusted with gain and offset
        :rtype: float
        """
        if self.time > (time % self.freq_in_seconds):
            self.fire_grain()
        self.time = time % self.freq_in_seconds
        return self.get_pcm_value(time) * self.gain + self.offset
