#!/usr/bin/env python
import sys

from os import path

from setuptools import find_packages
from setuptools import setup

needs_pytest = {'pytest', 'test', 'ptr'}.intersection(sys.argv)

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

test_requirements = []
with open(path.join(this_directory, 'test_requirements.txt')) as f:
    for line in f:
        require = line.split('#', 1)[0].strip()
        if require:
            test_requirements.append(require)

setup(
    name='hmm_profile',
    packages=find_packages(exclude=['tests']),
    version='0.0.10',
    url='https://github.com/Behoston/hmm_profile',
    license='MIT',
    author='Behoston',
    author_email='mlegiecki@gmail.com',
    description='Hidden Markov Model profile tools (reader/writer/data structures)',
    long_description=long_description,
    long_description_content_type='text/markdown',
    py_modules=['hmm_profile'],
    include_package_data=True,
    install_requires=['dataclasses;python_version<"3.7"'],
    tests_require=test_requirements,
    setup_requires=['pytest-runner'] if needs_pytest else [],
    platforms='any',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Other Environment',
        'Intended Audience :: Education',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Education',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Software Development',
        'Typing :: Typed',
    ],
)
