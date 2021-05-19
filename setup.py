from setuptools import find_packages
from setuptools import setup

setup(
    name='example-pkg-fredyeah',
    version='0.0.5',  # pylint: disable=undefined-variable
    description='example pkg',
    long_description='',
    url='https://github.com/fredyeah/py-modular',
    author='fred',
    author_email='example@example.com',
    license='mit',
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
