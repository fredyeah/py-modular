import soundfile as sf
import matplotlib.pyplot as plot
import numpy as np

def graph_node_lin(node, samples):
    """Used to graph a node's output with matplotlib over a given ammount of samples on a linear basis.

    :param node: A node that should be graphed over time
    :param samples: Number of samples the node should be graphed for
    :type samples: int
    """
    time = []
    samps = []
    for i in range(samples):
        # TODO: get sample rate from node?
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
    """Used to graph a node's output with matplotlib over a given ammount of samples on a logarithmic basis.

    :param node: A node that should be graphed over time
    :param samples: Number of samples the node should be graphed for
    :type samples: int
    """
    time = []
    samps = []
    for i in range(samples):
        # TODO: get sample rate from node?
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
    """Used to graph a transport over a given number of samples. Usefull for when events need to be seen visually

    :param tp: Transport that should be graphed
    :param samples: Number of samples the transport should be graphed for
    :type samples: int
    """
    samps = []
    time = []
    for i in range(samples):
        time.append(i)
    # TODO: get block size from transport
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
    """
    :param node: Node to be recorded
    :param filename: Name of the output file
    :type filename: string
    :param seconds: Number of seconds to record for
    :type seconds: int
    """
    buffer = []
    # TODO: get samplerate from node?
    for i in range(48000 * seconds):
        samp = node.get_sample(i / 48000.0) / 10.0
        buffer.append(samp)
    sf.write(filename, buffer, 48000)

def record_transport(tp, filename='recorded_session.wav', seconds=5):
    """
    :param tp: Transport to be recorded
    :param filename: Name of the output file
    :type filename: string
    :param seconds: Number of seconds to record for
    :type seconds: int
    """
    buffer = []
    blocks = int(seconds * 48000 / 1024)
    for i in range(blocks):
        print(str(i * 100 / blocks) + ' %')
        tp.get_block()
        buffer = buffer + tp.block
    sf.write(filename, buffer, 48000)
