import os
import numpy as np
import tensorflow.compat.v1 as tf
import tarfile
from random import randint
from magenta.models.nsynth import utils
from magenta.models.nsynth.wavenet import fastgen
from magenta.models.nsynth.wavenet.h512_bo16 import Config
from magenta.models.nsynth.wavenet.fastgen import generate_audio_sample
from magenta.models.nsynth.wavenet.fastgen import load_fastgen_nsynth
from magenta.models.nsynth.wavenet.fastgen import save_batch

def save_grain_cloud(grains, name='generated_grain_cloud'):
    """
    :param grains: Array of grains to save
    :type grains: array
    :param name: The name of the file without extension
    :type name: string
    """
    np.save(name, grains)

def encode_grains(grains, checkpoint: str):
    """
    :param grains: An array of audio data to be encoded
    :type grains: array(array)
    :param checkpoint: The name of the checkpoint to be used for encoding
    :type checkpoint: string
    :returns: An array of encoded grains
    :rtype: array
    """
    encodings = fastgen.encode(grains, checkpoint, len(grains[0]))
    return encodings

def mix_two_grains(grains):
    """
    :param grains: An array of encoded grains of the same size
    :type grains: array(2)
    :returns: A single grain
    :rtype: array
    """
    grain = (grains[0] + grains[1]) / 2.0
    return grain

def create_grains(file_name: str, file_location: str, grain_size=1024, grain_space=0, grain_offset=0, number_of_grains=8, checkpoint=None):
    """
    :param file_name: The name of the audio file to be granulated
    :type file_name: string
    :param file_location: The path where the audio file is located
    :type file_location: string
    :param grain_size: The size in samples of one grain
    :type grain_size: int
    :param grain_space: The size in samples of the chunck of audio to be granulated in the audio file
    :type grain_space: int
    :param grain_offset: The offset in samples of the start of the audio chuck to be granulated
    :type grain_offset: int
    :param number_of_grains: The number of grains to generate
    :type number_of_grains: int
    :param checkpoint: The model checkpoint which will be used for encoding the grains
    :type checkpoint: string
    :returns: An array of encoded grains
    :rtype: array
    """
    if grain_size < 512:
        raise Exception("minimum grain size is 512 samples")

    # TODO: make sample rate variable
    audio_file = utils.load_audio(os.path.join(file_location, file_name), sample_length=-1, sr=48000)
    audio_length = len(audio_file)

    if grain_space == 0:
        grain_space = audio_length

    if grain_size * 2 > grain_space:
        raise Exception("grain space must be at least twice the size of one grain")

    min_offset = grain_offset
    max_offset = grain_offset + grain_space

    if max_offset > audio_length:
        raise Exception("grain space plus offset should not be larger than the audio file")

    position_increment = grain_space // number_of_grains

    grain_positions_a = [randint(min_offset, max_offset) for i in range(number_of_grains)]
    grain_positions_b = [(i * position_increment) + grain_offset for i in range(number_of_grains)]

    grains_a = [audio_file[pos:(pos + grain_size)] for pos in grain_positions_a]
    grains_b = [audio_file[pos:(pos + grain_size)] for pos in grain_positions_b]

    grains_a = encode_grains(np.array(grains_a), checkpoint=checkpoint)
    grains_b = encode_grains(np.array(grains_b), checkpoint=checkpoint)

    grains_mixed = []
    for i in range(number_of_grains):
        grains_mixed.append([grains_a[i], grains_b[i]])
    return np.array([mix_two_grains(grains) for grains in grains_mixed])


def interpolate_grains(encoded_grains, number_of_grains=8):
    """
    :param encoded_grains: An array of encoded grains
    :type encoded_grains: array(2)
    :param number_of_grains: The number of grains to generate from interpolation
    :type number_of_grains: int
    :returns: An array of encoded grains
    :rtype: array
    """
    grain_a = encoded_grains[0]
    grain_b = encoded_grains[1]
    interpolated_grains = []

    for i in range(number_of_grains):
        weight_a = i / float(number_of_grains)
        weight_b = 1.0 - weight_a

        interpolated_grain = (grain_a * weight_a + grain_b * weight_b)
        interpolated_grains.append(interpolated_grain)

    return np.array(interpolated_grains)


def generate_grains(encoded_grains, checkpoint: str):
    """
    :param encoded_grains: A list of encoded grains to be synthesized back into audio
    :type encoded_grains: array
    :param checkpoint: The path and name of the checkpoint to use for synthesis
    :type checkpoint: string
    :returns: An array of audio buffers
    :rtype: array
    """
    session_config = tf.ConfigProto(allow_soft_placement=True)
    session_config.gpu_options.allow_growth = True

    with tf.Graph().as_default(), tf.Session(config=session_config) as sess:
        net = load_fastgen_nsynth(batch_size=encoded_grains.shape[0])
        saver = tf.train.Saver()
        saver.restore(sess, checkpoint)

        batch_size, encoding_length, _ = encoded_grains.shape
        hop_length = Config().ae_hop_length
        total_length = encoding_length * hop_length

        sess.run(net["init_ops"])

        audio_batch = np.zeros((batch_size, total_length), dtype=np.float32)
        audio = np.zeros([batch_size, 1])

        for i in range(total_length):
            encoding = i // hop_length
            audio = generate_audio_sample(sess, net, audio, encoded_grains[:, encoding, :])
            audio_batch[:, i] = audio[:, 0]
            if i % 100 == 0:
                print(str(i) + ' samples completed ')

        return audio_batch
