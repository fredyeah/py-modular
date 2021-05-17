How to create a sine wave with random pitch oscillation
==========================================================

First, import the proper oscillators and the `GlobalTransport` class which will hold everything together.
You can think of the `GlobalTransport` as a DAW session if you will.

.. literalinclude:: ../../examples/random_sine_wave.py
    :language: python
    :lines: 4-5

With `py-modular`, we generally start with control signals, and work our way down through oscillators, effects, and finally audio output.
Since we want our sine wave to change its pitch randomly, we will start with a random control signal.
We will use the `Random` oscillator for this.
In `py-modular`, oscillators should output between -1.0 and 1.0.
We are using the random oscillator as a control signal for another oscillator's frequency in Hz so we will want to make the gain larger.
A gain of 50.0 will give us a range of -50.0 to 50.0 Hz.

.. note::
    Generally, a negative frequency will translate to a wave inversion.

.. literalinclude:: ../../examples/random_sine_wave.py
    :language: python
    :lines: 7

Next, we will initialize the sine oscillator which will be the actual source of sound in the final product.
The frequency does not matter much in this situation, as we will be constantly changing it to random values.
We will leave the gain at 0.85 to allow a bit of headroom. 1.0 is generally very loud for gain.
Lastly, we include the random oscillator as an fmct list element.
This basically just says "we want the output of the random oscillator to control the frequency of the sine oscillator"

.. literalinclude:: ../../examples/random_sine_wave.py
    :language: python
    :lines: 8

Now we will create a global transport, which we said earlier can be thought of as a DAW session.
We will initialize the transport with default values, which will create two channels for us.
We can use the `add_node` method to add sounds to each channel.
This just adds the sine wave we created to the left and right channels, or channels 0 and 1.

.. literalinclude:: ../../examples/random_sine_wave.py
    :language: python
    :lines: 10-12

Finally we call the `start` method of the transport, which will begin an audio processing thread.

.. literalinclude:: ../../examples/random_sine_wave.py
    :language: python
    :lines: 14

Try running the script with `python random_sine_wave.py`, you should hear a sine wave changing smoothly in pitch.
