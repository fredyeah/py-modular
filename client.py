from socket import *
from time import sleep
import threading
import sounddevice as sd
import soundfile as sf
import numpy as np
import struct

s = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
s.setsockopt(SOL_SOCKET, SO_REUSEPORT, 1)
s.bind(("",2000))

def callback(indata, outdata, frames, time, status):
    data,addr = s.recvfrom(2048)
    d = struct.unpack('512f', data)
    d = list(d)
    arry = np.array(d, dtype='f4').reshape((512, 1))
    outdata[:] = arry

s.sendto(b'hello', ('165.227.151.149', 5000))
while True:
    with sd.Stream(channels=1, callback=callback):
        sd.sleep(9375)
