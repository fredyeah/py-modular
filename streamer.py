from socket import *
from time import sleep
import threading
import struct
import sounddevice as sd
import soundfile as sf

s = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
s.setsockopt(SOL_SOCKET, SO_REUSEPORT, 1)
s.bind(("",5000))

def send_sunny():
    bin,fs = sf.read('sunny.wav')
    data,addr = s.recvfrom(512)
    b_count = 0
    fs = 48000
    arry = []
    freq = 800
    dc = freq / 2
    while True:
        for i in range(512):
            index = b_count * 512
            arry.append(bin[i+index][0])
        b_count = b_count + 1
        d = struct.pack('512f', *arry)
        s.sendto(d, addr)
        arry = []
        sleep(0.01)

send_sunny()
