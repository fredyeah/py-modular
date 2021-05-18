Recording audio to a .wav file
==========================================================

Recording the output from a `GlobalTransport` is relatively simple.
We will copy most of the code from the last tutorial to demonstrate.

.. literalinclude:: ../../examples/record_audio.py
    :language: python
    :lines: 4-37



.. hint::
    Since we are not concerned with real time performance while writing a .wav file, we can bump up the number of pings.

    .. literalinclude:: ../../examples/record_audio.py
        :language: python
        :lines: 24

To record the audio, we simply need to call the `record_transport` method with the global transport.
We can also define the number of seconds to record and the file name.

.. literalinclude:: ../../examples/record_audio.py
    :language: python
    :lines: 39

That's it! There should be a new .wav file in the working directory with your recorded audio.
The output should sound something like this

.. raw:: html

    <audio controls="controls">
        <source src="../_static/record_audio.wav" type="audio/wav">
    </audio>
