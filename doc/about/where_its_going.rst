What does the future of the project look like?
===============================================

.. centered:: The general road map for optimization

One of the first tasks that I would like to complete is getting the real time performance to a more acceptable level.
So far, it seems that the best way to go would be writing most of the DSP routines in C and using CFFI to integrate with Python_.
This would also open up opportunities to port the code and concept to other platforms.
One platform that would work well with this concept is eurorack_.

I also would like to create a more user-friendly interface for the project.
I do not want to take the project fully into the visual and GUI domain,
but I would like to implement some sort of syntax and wrapper around the project so that knowing Python_ is not mandatory to use py-modular.

.. centered:: Features in the future

Because the nature of py-modular is more focused around trying new ideas, it is hard to tell exactly where the project will go.
One project that I am currently working on is a series of physics emulation tools.
I would like to bring these into the project so thing things like sequencing melodies based off particle collision simulations can be accomplished.

I also would like to explore the AI domain more.
Magenta_ has many more models that could fit within this project nicely, the GANSynth_ in particular is very interesting.
There are also other AI music projects that I would like to explore, and continue to see where they fit into creative processes.

Something that I think py-modular is missing, is more mature event sequencing abilities.
The unique part about py-modular is the ability to programmatically create sounds, and to define synthesizers with text.
What is lacking, though, is the ability to programmatically sequence events in a way that doesn't become repetitive after the first few seconds or minutes.
Some more esoteric sequencing nodes and more exploration in event types would greatly benefit the project and concept.

.. centered:: Projects using this project

One thing that I would like to create with the project is a generative sample creator.
This plays into a longterm goal to create auto-generated music streams,
but generating short samples of music to be used in projects is far more achievable as a first step.
The idea would be that samples could be generated given a few key words that would map to certain combinations of nodes.

These goals, however, are only my own.
My biggest goal is to see the project become something more than my own creation.

.. _eurorack: https://en.wikipedia.org/wiki/Eurorack

.. _Python: https://www.python.org/

.. _Magenta: https://magenta.tensorflow.org/

.. _GANSynth: https://magenta.tensorflow.org/gansynth
