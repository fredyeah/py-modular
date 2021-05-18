Use the grain cloud to create textures
=====================================================================

This tutorial will show you briefly what can be done with the generated grain cloud from the previous tutorial.
Essentially, we now have a collection of very small pieces of AI generated audio which we can then try to reassemble into a larger audio sample.

.. note::
    Keep in mind that this is still largely an experimental project.
    You will likely end up with many samples that just sound like noise, but if you can tweak the parameters just right, there can be very interesting results.

We will start, like always, with imports.

.. literalinclude:: ../../../examples/generative/synthesize_cloud.py
    :language: python
    :lines: 4-9

We can then load our grain cloud with `numpy` and window the grains.
We will use `window_grains_sin` to add fade ins and outs to each grain.
This only makes a subtle difference in how smooth the grains sound, but it is good to have.

.. literalinclude:: ../../../examples/generative/synthesize_cloud.py
    :language: python
    :lines: 11-12

We can use the `GranBase` node to create a granular synthesizer.
We need to supply it only with a set of grains.
We will also add some jitter which will help remove any unwanted rhythms that appear as a result of granular synthesis.

.. literalinclude:: ../../../examples/generative/synthesize_cloud.py
    :language: python
    :lines: 14

As a last step to the signal chain, we will add two delays with multiple lengths to create a sort of reverb effect.
This is essentially emulating old bucket brigade delay chips.

.. literalinclude:: ../../../examples/generative/synthesize_cloud.py
    :language: python
    :lines: 16-24

Making two slightly different delays and adding them to separate channels will give a nice stereo effect to our grain texture.

.. literalinclude:: ../../../examples/generative/synthesize_cloud.py
    :language: python
    :lines: 26-29

Lastly, we can play and record the audio. It should sound something like the following if you used the same .wav file

.. raw:: html

    <audio controls="controls">
        <source src="../_static/synthesize_cloud.wav" type="audio/wav">
    </audio>
