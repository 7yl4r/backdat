#!/usr/bin/env python

from setuptools import setup
import io

import backdat

def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)

long_description = read('README.md') #, 'CHANGES.txt')

setup(name='backdat',
    version=backdat.__version__,
    description='back dat data up declaratively',
    long_description=long_description,
    author='Tylar Murray',
    author_email='code+backdat@tylar.info',
    url='https://github.com/7yl4r/backdat',

    tests_require=['nose'],
    install_requires=[
        "croniter"
    ],
    #cmdclass={'test': PyTest},

    packages=['backdat']
)
