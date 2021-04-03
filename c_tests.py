from ctypes import *
import math

tests = CDLL('./sine.so')
tests.sine_node.restype = c_float
print(tests.sine_node(c_float(0.1)))
