How py-modular came about
=============================

In the true spirit of modularity, the project started as many different projects that have become one.
Originally, the base of the project was a virtualization of eurorack and modular synthesis.
Many of the concepts are the same, where instruments are built using smaller nodes and concepts.
When switching from macOS to Linux, the base project also became more of an artistic outlet for me because I lost my tried and tested Ableton Live.

.. note::
    Ableton, if you're reading this, please support Linux soon.

After becoming inspired by the interesting combination of Python and creative audio,
I took up another project centered around artificial intelligence and music.
I think it will be a long time before AI finds its place in music (I say that before the release of this project),
but it is also important to embrace new technologies and find out what they have to offer with open minds.
The AI project became more centered around the Magenta project, and eventually more specifically around granulation.
The concept behind this came after trying to use the Magneta Nsynth models to try and generate audio samples longer than a second.
Nsynth took me around 1 minute per second of generated audio, and this was on a well performing, GPU enabled computer.
While I'm sure there were better ways to optimize, and I'm sure I will integrate different aproaches into the project in the future,
granular synthesis seemed to be a much more inviting way to go in comparison to raw audio generation.

.. centered:: Why granular synthesis?

First, granular synthesis works on the basis of very small pieces of audio.
This provided the project with two benefits.
The small pieces of audio can be rearranged however many times you want to create seemingly larger pieces of audio.
Additionally, since GPUs and the Nsynth model are more optimized for parallel processing,
it took almost the same time to processes 128 times 1024 sample lengths of audio as it did to process just 1 times 1024 sample length audio buffer.
Though the results are still far from real time performance, interesting results can still be generated in a reasonable amount of time.

.. centered:: How the projected ended up in its current state

As a hobbyist developer and musician, I end up having a lot of small projects that pile up and never get out into the world.
py-modular has become an outlet for me, technically and creatively, to publish experimental works.
The first two projects were AI granular synthesis and eurorack emulation, but there will be many more I'm sure.
It is also my hope as the project creator that anyone else who is interested can contribute their ideas that would maybe never get published otherwise. 
