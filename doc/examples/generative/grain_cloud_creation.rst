Creating a grain cloud for granular synthesis using Magenta's Nsynth
=====================================================================

`py-modular` is primarily an experimental project, aimed at exploring how new technologies fit into the arts industries.
One inspiration for the project has been the Magenta project, an open source project centered around AI in creative practices.
This tutorial will show you how to use some small wrappers around Magenta to generate new and hybrid sounds from pre-existing sounds.

.. warning::
    Magenta is a big project, also built on top of Tensorflow, another very large project.
    We recommend to follow the instructions on the Magenta Github page for installation, as we do not include Magenta as a `py-modular` requirement.

For creating grain clouds, it is likely necessary to have a CUDA capable GPU.

.. note::
    While developing this project, we are able to generate 128 grains of length 1024 in a bit less than a minute on a GTX 1070.
    This is moderately sufficient for granular synthesis.

Our first steps are to set which GPU we want to use for compute.
You can skip this step if you don't have a GPU but it will take far longer to generate grains.
We will then import some utility functions from the `generative` module

.. literalinclude:: ../../../examples/generative/grain_cloud_creation.py
    :language: python
    :lines: 4-6

We will need to download one of the pre-trained models from the Magenta project to create audio.
You can download a pretrained model here_, then just extract the file to your working directory.
You should have a new folder called `wavenet-ckpt` which will contain the model checkpoints.
You also will need a .wav file to granulate placed in your working directory. For our example, we will use `debussy_printemp.wav`.

.. _here: http://download.magenta.tensorflow.org/models/nsynth/wavenet-ckpt.tar

The first step is to create the grains.
We can call `create_grains` with some parameters to build our grain cloud.
Because we want to generate grains interpolated between two audio samples, we will set the number of grains here to 2.

.. hint::
    If you would rather granulate through time, you can increase the number of grains in this step and skip the interpolation step.

This function loads our audio, mixes it up a bit, then encodes the audio using `magenta.models.nsynth.wavenet.fastgen` so it is readable by the model.
If you want to know more about how Nsynth works, Magenta has great documentation on their website.

Next, since we want to granulate between two sounds, we will create a number of grains using interpolation.
This is where it gets interesting.
Since the data we are interpolating is encoded at this point, interpolation in the encoded domain will produce different results than interpolation in the raw data domain.

.. literalinclude:: ../../../examples/generative/grain_cloud_creation.py
    :language: python
    :lines: 9

We will then generate the new audio using the `generate_grains` method with the encoded audio.
This is essentially a modified version of `magenat.models.nsynth.wavenet.fastgen.synthesize` that returns raw audio data instead of saving a .wav file.

.. literalinclude:: ../../../examples/generative/grain_cloud_creation.py
    :language: python
    :lines: 10

Lastly, we can save our grains as a `numpy` binary file and load them into a synthesizer in the next tutorial.

.. literalinclude:: ../../../examples/generative/grain_cloud_creation.py
    :language: python
    :lines: 11
