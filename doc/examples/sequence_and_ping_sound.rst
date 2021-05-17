Create a ping sound with multiple fm controls
==============================================================

For this tutorial, we need to import the following:

.. literalinclude:: ../../examples/sequence_and_ping_sound.py
    :language: python
    :lines: 4-9

First, we will create our envelopes which you should be familiar with.
This time, we will also use the `ExpEnv` in tandem with the `Random` oscillator.
We will use one envelope to control a slight pitch variation over time, one to control a attack/decay type movement with pitch, and one to control gain.
The `ExpEnv` class is unique because it can be controlled using an event sequencer or event handler.

.. literalinclude:: ../../examples/sequence_and_ping_sound.py
    :language: python
    :lines: 11-13

To control the pitch and gain attack/decay envelopes, we will use a `TriggerEvent`.
Both envelopes can be placed into the same trigger event so that they fire at the same time.
An `EventSequencer` is then used to control when the event is fired.
An array of arbitrary length is used to determine when events are fired.

.. note::
    The sequence parameter of the `EventSequencer` class controls when the events are fired.
    If the sequence is `[900, 100, 300]`, the first event will fire at 900 samples, the second event will fire 100 samples after the first event, the third event will fire 300 samples after the second event, etc...

.. literalinclude:: ../../examples/sequence_and_ping_sound.py
    :language: python
    :lines: 15-16

We will then build the ping sound with a triangle wave.
We can assign the gain envelope to the triangle's `gainct`, and we can just put both pitch envelopes in a list and assign it to the `fmct`.
They will both control the frequency.

.. literalinclude:: ../../examples/sequence_and_ping_sound.py
    :language: python
    :lines: 18

Last, we follow the same steps as before to initiate the global transport and start it.
This time, however, we also have some seuqnces that we want to fire during the session.
We can put the sequencer into a list and assign it as one of the event handlers in the global transport.
This will make sure that the events are synced to the session on a sample by sample basis.

.. literalinclude:: ../../examples/sequence_and_ping_sound.py
    :language: python
    :lines: 20-24
