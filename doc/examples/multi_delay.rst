Using more effects and programmatic sound system creation
==========================================================

This tutorial will go into some more interesting use cases for `py-modular` and hopefully demonstrate concepts where `py-modular` can shine in comparison to traditional music creation environments.
We will be building off the previous tutorials, and implementing some more effects and programmatic system designs.
First, we need to import some nodes to create the sound system and a utility function to generate random numbers.

.. literalinclude:: ../../examples/multi_delay.py
    :language: python
    :lines: 4-12

We will essentially copy most of the design from the last tutorial and implement it as a function.
Each time we call this function, we will create another instance of the ping sound, but each created instance will be slightly different because of the random oscillator.
Additionally, we will use the `randint` method to generate random event sequences for each instance of the ping sound.

.. literalinclude:: ../../examples/multi_delay.py
    :language: python
    :lines: 14-21

Then we will define some number of pings to create.
This can be any number, but since `py-modular` is not very optimized for real time performance at the time of writing this, the larger the number, the more audio buffer underruns will occur.
Even with just one ping, we should get an interesting result.
We also will create some lists so that we can store ping and event instances along the way

.. literalinclude:: ../../examples/multi_delay.py
    :language: python
    :lines: 23-25

We can iterate through our number of pings to create and store the returned instances in the previous lists.

.. literalinclude:: ../../examples/multi_delay.py
    :language: python
    :lines: 27-30

Then we add in the best part, the `MultiChannelDelay`.
The delay takes an array of sounds to be processed, in this case our generated pings, a list of delay times for each channel in samples, and a value for delay feedback.
For feedback, somewhere between 1.1 and 1.3 will give a good atmospheric result.

.. literalinclude:: ../../examples/multi_delay.py
    :language: python
    :lines: 32

We can then create our global transport with the event handlers.
To add the delay, we will just add the node to both channels of the global transport.
Since it is a multichannel delay, it will take care of deciding which sounds go to which channels.

.. literalinclude:: ../../examples/multi_delay.py
    :language: python
    :lines: 34-38

.. warning::
    Since `py-modular` is not optimized for real time performance yet, this tutorial may perform poorly on computers that are not high performance.
    We recommend using the recording utilities to create .wav files and listen back to the results that way for now.

The output should be similar to this, keeping in mind the pitches are randomly generated 

.. raw:: html

    <audio controls="controls">
        <source src="../_static/multi_delay.wav" type="audio/wav">
    </audio>
