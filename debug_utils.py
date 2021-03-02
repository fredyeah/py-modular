import soundfile as sf
import matplotlib.pyplot as plot

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

def record_file(node, filename='recorded_wave.wav', seconds=5):
    buffer = []
    for i in range(48000 * seconds):
        samp = node.get_sample(i / 48000.0) / 10.0
        buffer.append(samp)
    sf.write(filename, buffer, 48000)
