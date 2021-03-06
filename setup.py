#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from __future__ import absolute_import, print_function

import io
import os
import re
from glob import glob
from os.path import basename
from os.path import dirname
from os.path import join
from os.path import relpath
from os.path import splitext

from setuptools import find_packages
from setuptools import setup


def read(*names, **kwargs):
    return io.open(
        join(dirname(__file__), *names),
        encoding=kwargs.get('encoding', 'utf8')
    ).read()


setup(
    name='montague_toml',
    version='0.2.0',
    license='BSD',
    description=("Montague provides functions to load WSGI apps and servers "
                 "based on configuration files. montague_toml loads configuration "
                 "from TOML markup files."),
    long_description=('%s\n%s' % (read('README.rst'),
                                  re.sub(':[a-z]+:`~?(.*?)`', r'``\1``',
                                         read('CHANGELOG.rst')))),
    author='Jon Rosebaugh',
    author_email='jon@inklesspen.com',
    url='https://github.com/inklesspen/montague_toml',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        "License :: OSI Approved :: MIT License",
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
        'Topic :: Utilities',
    ],
    keywords=[
        # eg: 'keyword1', 'keyword2', 'keyword3',
    ],
    install_requires=[
        'montague>=0.2.0',
        'pytoml>=0.1.2',
    ],
    extras_require={
        # eg: 'rst': ['docutils>=0.11'],
    },
    entry_points={
        "montague.config_loader": [
            "toml = montague_toml.toml:TOMLConfigLoader"
        ],
        'console_scripts': [
        ]
    },
)
