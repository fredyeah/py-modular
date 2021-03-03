import soundfile as sf
import matplotlib.pyplot as plot
import numpy as np

def graph_node_lin(node, samples):
    time = []
    samps = []
    for i in range(samples):
        sample = node.get_sample(i/48000.0)
        samps.append(sample)
        time.append(i)
    plot.plot(time, samps)
    plot.title('wave')
    plot.xlabel('sample')
    plot.ylabel('amplitude')
    plot.grid(True, which='both')
    plot.axhline(y=0, color='k')
    plot.show()

def graph_node_log(node, samples):
    time = []
    samps = []
    for i in range(samples):
        sample = node.get_sample(i/48000.0)
        samps.append(sample)
        time.append(i)
    plot.plot(time, samps)
    plot.title('wave')
    plot.yscale('log')
    plot.xlabel('sample')
    plot.ylabel('amplitude')
    plot.grid(True, which='both')
    plot.axhline(y=0, color='k')
    plot.show()

def graph_transport(tp, samples):
    samps = []
    time = []
    for i in range(samples):
        time.append(i)
    for i in range(int(samples / 1024)):
        b = tp.get_block()
        for x in range(len(b)):
            samps.append(b[x])
    plot.plot(time, samps)
    plot.title('wave')
    plot.yscale('log')
    plot.xlabel('sample')
    plot.ylabel('amplitude')
    plot.grid(True, which='both')
    plot.axhline(y=0, color='k')
    plot.show()

def record_file(node, filename='recorded_wave.wav', seconds=5):
    buffer = []
    for i in range(48000 * seconds):
        samp = node.get_sample(i / 48000.0) / 10.0
        buffer.append(samp)
    sf.write(filename, buffer, 48000)

def record_transport(tp, filename='recorded_session.wav', seconds=5.0):
    buffer = [[],[]]
    blocks = int(seconds * 48000 / 1024)
    for i in range(blocks):
        buffer = tp.get_block()
    sf.write(filename, buffer, 48000)
