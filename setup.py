#! /usr/bin/env python

from __future__ import absolute_import, print_function, division
try:
    from setuptools import setup, find_packages
except ImportError:
    raise RuntimeError('No suitable version of setuptools detected.')
import codecs
import os

HERE = os.path.abspath(os.path.dirname(__file__))

CLASSIFIERS = [
    'Natural Language :: English',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.5',
    'Topic :: Software Development :: Libraries :: Python Modules'
]

###############################################################################


def read(*parts):
    with codecs.open(
        os.path.join(HERE, *parts), 'rb', 'utf-8'
    ) as file_pointer:
        return file_pointer.read()


setup(
    name='gkit_cogs',
    version='0.9.0',
    url='https://github.com/gannon93/gkit_cogs',
    license='MIT',
    author='Zachary Gannon',
    author_email='zachgannon93@gmail.com',
    description='Cogs written for Red-DiscordBot by @Twentysix26',
    keywords=[],
    long_description=read(* ['README.md']),
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    zip_safe=False,
    classifiers=CLASSIFIERS,
    include_package_data=True,
    test_suite='tests')
