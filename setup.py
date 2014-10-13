#!/usr/bin/env python

from setuptools import setup, find_packages

import os

requires = [
]


setup(
    name='killbill',
    version=open(os.path.join('killbill', '_version')).read(),
    description='Tools for processing AWS detailed billing reports',
    long_description=open('README.md').read(),
    author='Mitch Garnaat',
    author_email='mitch@scopely.com',
    url='https://github.com/scopely-devops/killbill',
    packages=find_packages(exclude=['tests*']),
    package_dir={'killbill': 'killbill'},
    install_requires=requires,
    license=open("LICENSE").read(),
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4'
    ),
)
