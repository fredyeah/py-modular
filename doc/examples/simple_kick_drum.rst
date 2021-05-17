How to create a basic kick drum with pitch and gain envelopes
==============================================================

First, we need to import some oscillators and the `GlobalTransport`, like in the previous tutorial.
We will also need some effects processors to control gain and signal linearity.

.. literalinclude:: ../../examples/simple_kick_drum.py
    :language: python
    :lines: 4-6

We will start by writing a quick wrapper to easily create envelopes.
For the purpose of this tutorial, we will be shaping a saw wave and using it as an envelope, but there are many other ways it could be done.
Since we want our envelopes to go from high to low, we will apply a gain of -1.0 to the saw signal to invert it.
After creating a saw wave, we can use the `LinToExp` effect node to shape the wave.
Adding a curve parameter to the processor will allow us to turn a linear signal into an exponential or logarithmic-type signal.
Lastly, we will put the signal through an attenuator.

.. literalinclude:: ../../examples/simple_kick_drum.py
    :language: python
    :lines: 8-12

For the gain envelope, we want the gain to be above 0, since a negative gain will only invert the wave.
Since the saw wave we are basing these envelopes on oscillate between -1.0 and 1.0, we need a gain and offset of 0.5 to transform the signal into the 0.0 to 1.0 range.

.. literalinclude:: ../../examples/simple_kick_drum.py
    :language: python
    :lines: 14

For the pitch envelope, since we are working in Hz, we will increase the gain and offset substantially, so we can be sure it will be in our auditory range.

.. literalinclude:: ../../examples/simple_kick_drum.py
    :language: python
    :lines: 15

To complete the kick, we will use another sine wave as a base and apply the gain and pitch envelopes correspondingly.

.. literalinclude:: ../../examples/simple_kick_drum.py
    :language: python
    :lines: 17

To complete it, we can follow the same steps as the last tutorial to play our audio.
Put everything in the global transport, then run `python simple_kick_drum.py` and you should hear a kick sound.

.. literalinclude:: ../../examples/simple_kick_drum.py
    :language: python
    :lines: 19-23
