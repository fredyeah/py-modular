from math import floor, asin, sin, pi

def window_grains_sin(grains=[]):
    """Util used to window an array of audio with half a sine wave

    :param grains: An array of audio buffers that contain audio data to be windowed
    :type grains: array(array)
    :returns: An array of the same shape as the input, but windowed
    :rtype: array(array)
    """
    for grain in grains:
        grain_length = len(grain)
        for i in range(grain_length):
            grain[i] = grain[i] * sin(i * pi / grain_length)
    return grains

def window_grains_tri(grains=[]):
    """Util used to window an array of audio with half a triangle wave

    :param grains: An array of audio buffers that contain audio data to be windowed
    :type grains: array(array)
    :returns: An array of the same shape as the input, but windowed
    :rtype: array(array)
    """
    for grain in grains:
        grain_length = len(grain)
        for i in range(grain_length):
            grain[i] = grain[i] * (asin(sin(i * pi / grain_length)) / (0.5 * pi))
    return grains
