from math import floor, asin, sin, pi

def window_grains_sin(grains=[]):
    for grain in grains:
        grain_length = len(grain)
        for i in range(grain_length):
            grain[i] = grain[i] * sin(i * pi / grain_length)
    return grains

def window_grains_tri(grains=[]):
    for grain in grains:
        grain_length = len(grain)
        for i in range(grain_length):
            grain[i] = grain[i] * (asin(sin(i * pi / grain_length)) / (0.5 * pi))
    return grains
