from setuptools import find_packages
from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='py-modular',
    version='0.0.1',
    description='An experimental, modular audio programming environment in python',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/fredyeah/py-modular',
    author='Frederic',
    author_email='mark.s@catalyst-students.com',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    install_requires=[
        'cffi',
        'cycler',
        'kiwisolver',
        'matplotlib',
        'numpy',
        'Pillow',
        'pycparser',
        'pyparsing',
        'python-dateutil',
        'six',
        'sounddevice',
        'SoundFile'
    ]
)
